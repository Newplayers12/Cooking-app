from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django import forms

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

# TODO: Account Model
class SignupForm(UserCreationForm):
    fullname = forms.CharField(max_length=150, required=True)
    class Meta:
        model = User
        fields = ['fullname', 'username', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        ph = ['Full name', 'Username', 'Email', 'Password', 'Confirm Password']
        for field_items, stn in zip(self.fields.items(), ph):
            self.fields[field_items[0]].help_text = None
            self.fields[field_items[0]].label = ""
            self.fields[field_items[0]].widget.attrs['class'] = 'input-shape-signup'
            self.fields[field_items[0]].widget.attrs['placeholder'] = stn
    
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        username = cleaned_data.get('username')
        errors = []
        dup_username = User.objects.filter(username=username)
        dup_email = User.objects.filter(email=email)
        if dup_username:
            errors.append(ValidationError("Username was already taken.", code="username_invalid"))
        if dup_email:
            errors.append(ValidationError("Email was already signed up.", code="email_invalid"))
        if errors:
            raise ValidationError(errors)
            
class ProfileForm(UserCreationForm):
    pass