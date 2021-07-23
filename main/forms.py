from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Question, Response
from django import forms


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'email': forms.EmailInput(attrs={
                'required': True,
                'placeholder': 'john@example.com',
                'autofocus': True
            }),
            'username': forms.TextInput(attrs={
                'placeholder': 'John Smiths',
            })
        }

    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs = {'placeholder': 'Password'}
        self.fields['password2'].widget.attrs = {
            'placeholder': 'Re-enter password'}


class LoginForm(AuthenticationForm):
    class Meta:
        fields = '__all__'


class NewQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'body']
        widgets = {
            'title': forms.TextInput(attrs={
                'autofocus': True,
                'placeholder': 'What is the solution to this binomial equation?'
            })
        }


class NewResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['body']


class NewReplyForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Please enter your response'
            })
        }
