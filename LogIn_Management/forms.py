from django import forms

class LogIn_Form(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
