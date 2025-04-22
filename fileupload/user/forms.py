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
        fields = ['title', 'subject', 'body']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'autofocus': True,
                'placeholder': 'Your question title',
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Subject area of the question',
            }),
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your question in detail...',
                'rows': 5,
            }),
        }

class NewResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['body', 'pdf']
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your response...',
                'rows': 4,
            }),
            'pdf': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
        }
    
    
class SiteUsersForm(forms.ModelForm):
    class Meta:
        model = SiteUsers
        fields = '__all__'
        exclude = ['user']