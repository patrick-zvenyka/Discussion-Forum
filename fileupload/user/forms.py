from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.db import models
from .models import Question, Response, SiteUsers

class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'placeholder': '@jandoe',
            'class': 'form-control'
        })
        self.fields['email'].widget.attrs.update({
            'placeholder': 'jandoe@gmail.com',
            'class': 'form-control'
        })
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Password',
            'class': 'form-control'
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Confirm Password',
            'class': 'form-control'
        })


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'placeholder': '@jandoe',
            'class': 'form-control'
        })

        self.fields['password'].widget.attrs.update({
            'placeholder': 'Password',
            'class': 'form-control'
        })

class NewQuestionForm(forms.ModelForm):
   
    class Meta:
         model = Question
         fields = ['title','subject','body']

         widgets ={
             'title':forms.TextInput(attrs={
                 'autofocus' : True,
                'placeholder' : 'Your question title',
                })
         }

class NewResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['body','pdf']
    
    
class SiteUsersForm(forms.ModelForm):
    class Meta:
        model = SiteUsers
        fields = '__all__'
        exclude = ['user']