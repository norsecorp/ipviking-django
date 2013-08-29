from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(required = True)
    password = forms.CharField(required = True)
    
class EmailForm(forms.Form):
    email = forms.EmailField(required = True, label = "Email (Note: your session will be monitored)")



