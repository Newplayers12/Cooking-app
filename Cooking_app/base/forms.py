from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm

class MyPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(MyPasswordResetForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'class': 'input-template',
            'placeholder': 'Email',
        })

class MySetPasswordForm(SetPasswordForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        self.fields['new_password1'].label = ''
        self.fields['new_password2'].label = ''
        self.fields['new_password1'].help_text = None
        self.fields['new_password2'].help_text = None
        self.fields['new_password1'].widget.attrs.update({
            'class': 'input-template',
            'placeholder': 'New password',
        })
        self.fields['new_password2'].widget.attrs.update({
            'class': 'input-template',
            'placeholder': 'Re-enter the password',
        })
