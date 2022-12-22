from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.forms import ModelForm
from django import forms

from .models import UserInfo, Post    


class LoginForm(forms.Form):
    username = forms.CharField(
        label="", 
        max_length=150, 
        widget=forms.TextInput(attrs={
            'class': 'input-shape-login', 
            'placeholder': 'Username',
        })
    )
    password = forms.CharField(
        label="", 
        widget=forms.PasswordInput(attrs={
            'class': 'input-shape-login', 
            'placeholder': 'Password',
        })
    )

class SignupForm(UserCreationForm):
    fullname = forms.CharField(max_length=150, required=True)
    class Meta:
        model = User
        fields = ['fullname', 'email', 'username',
                  'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(SignupForm, self).__init__(*args, **kwargs)
        placeholder = ['Full name', 'Email', 'Username',
                       'Password', 'Confirm Password']
        for field_items, ph in zip(self.fields.items(), placeholder):
            self.fields[field_items[0]].help_text = None
            self.fields[field_items[0]].label = ""
            self.fields[field_items[0]].widget.attrs['class'] = 'input-shape-signup'
            self.fields[field_items[0]].widget.attrs['placeholder'] = ph
    
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        username = cleaned_data.get('username')
        dup_username = User.objects.filter(username=username)
        dup_email = User.objects.filter(email=email)
        if dup_email:
            messages.error(self.request, "Email was already signed up.")
        if dup_username:
            messages.error(self.request, "Username was already taken.")
        if dup_email or dup_username:
            raise ValidationError(message="Invalid Information", code="invalid")

    def save(self, commit=True):
        user = super(SignupForm, self).save(commit=False)
        if commit:
            user.save()
            UserInfo.objects.create(
                user=user, 
                fullname=self.cleaned_data['fullname'],
            )
        return user


class ProfileForm(ModelForm):
    pass

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(PostForm, self).__init__(*args, **kwargs)
        

        