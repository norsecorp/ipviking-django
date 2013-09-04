from django.views.generic import View
from ipviking_django.views import BaseView
from django.shortcuts import render_to_response


class HomeView(View):
    def get(self, request):
        return render_to_response('home.html', {})
    def post(self, request):
        return render_to_response('home.html')
    
class NextView(BaseView):
    def get(self, request):
        return render_to_response('next.html', {})
        

    
    
