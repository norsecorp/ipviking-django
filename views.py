# Create your views here.
from django.views.generic import View
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.shortcuts import render_to_response
from django.utils.decorators import classonlymethod
from ipviking_auth.auth_rules import ipv_action
from ipviking_auth.forms import LoginForm, EmailForm
from functools import update_wrapper

class BaseView(View):
    """This is a base class designed to implement the IPViking check"""
    
    @classonlymethod
    def as_view(cls, **initkwargs):
        """
        We're going to add our check into View.as_view() to ensure it's used at every page
        """
        # sanitize keyword arguments
        for key in initkwargs:
            if key in cls.http_method_names:
                raise TypeError("You tried to pass in the %s method name as a "
                                "keyword argument to %s(). Don't do that."
                                % (key, cls.__name__))
            if not hasattr(cls, key):
                raise TypeError("%s() received an invalid keyword %r. as_view "
                                "only accepts arguments that are already "
                                "attributes of the class." % (cls.__name__, key))

        def view(request, *args, **kwargs):
            ipv_allow = request.session.get('ipviking')
            if ipv_allow != 0:
                #Visitor hasn't been checked out
                response = AuthView().get(request)
                if not response:
                    #let it fall through to dispatch
                    pass
                else:
                    return response
            self = cls(**initkwargs)                
            if hasattr(self, 'get') and not hasattr(self, 'head'):
                self.head = self.get
            self.request = request
            self.args = args
            self.kwargs = kwargs
            return self.dispatch(request, *args, **kwargs)

        # take name and docstring from class
        update_wrapper(view, cls, updated=())

        # and possible attributes set by decorators
        # like csrf_exempt from dispatch
        update_wrapper(view, cls.dispatch, assigned=())
        return view

class AuthView(View):
    def get(self, request):
        if not request.session.get('ipviking') == 0:
            ip = request.get_host().split(':')[0] # sanitize port off the end
            if '127.0.0.1' in ip:    
                ip = '208.74.76.5' #overwriting for testing cause 127.0.0.1 is not valid
            context = ipv_action(request, ip)
            request = context.pop('request')
            try:
                template = context.pop('template')
                return render_to_response(template, context)
            except KeyError:
                pass
        return HttpResponseRedirect(request.path, context)
        
    def post(self, request): 
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        if username and password:
            form = LoginForm(request.POST)
            if form.is_valid():
                user = authenticate(username, password)
                if user is not None:
                    login(user, request)
                    request.session['ipviking'] = 0
                    return render_to_response('home', {'request':request})
            form = LoginForm()
            state = "Invalid username/password."
            return render_to_response('auth.html', {'state':state, 'form':form})
        
        elif email:
            form = EmailForm(request.POST)
            if form.is_valid():
                request.session['email'] = email
                request.session['ipviking'] = 0
                return render_to_response('home.html', {})
            else:
                form = EmailForm()
                state = "Invalid email address."
                return render_to_response('auth.html', {'form':form, 'state':state})
        else:
            return render_to_response('home.html', state = 'Invalid responses.')