from django.views.generic import View
BaseView = __import__('ipviking-django.views.BaseView')
from django.shortcuts import render_to_response


class HomeView(View):
    def get(self, request):
        return render_to_response('home.html', {})
    def post(self, request):
        return render_to_response('home.html')
    
class NextView(BaseView):
    def get(self, request):
        return render_to_response('next.html', {})
        

class AuthView(View):
    def get(self, request, context):
        template = context.pop('template')
        return render_to_response(template, context)

        
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