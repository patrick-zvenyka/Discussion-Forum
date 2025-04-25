from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.db import models
from .models import Question, Response, SiteUsers, Subject

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
    subject = forms.ModelChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Subject',
        empty_label="Select a subject",
    )

    class Meta:
        model = Question
        fields = ['title', 'subject', 'body']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'autofocus': True,
                'placeholder': 'Your question title',
            }),
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your question in detail...',
                'rows': 5,
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize how the subject appears in the dropdown
        self.fields['subject'].label_from_instance = lambda obj: f"{obj.code} - {obj.name}"

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
        widgets = {
            'position': forms.TextInput(attrs={
                'class': 'form-control',
                'autofocus': True,
                'placeholder': 'Your position',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your email',
            }),
            'program': forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Your program'
            }),
            'pro_pic': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            })
        }