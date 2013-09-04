"""Contains our user authentication forms"""
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label = 'Username')
    password = forms.CharField(label = 'Password', widget = forms.PasswordInput)

class EmailForm(forms.Form):
    email = forms.EmailField()
    