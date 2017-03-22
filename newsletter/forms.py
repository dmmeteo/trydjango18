from django import forms
from .models import SignUp

class ContactForm(forms.Form):
    full_name = forms.CharField(required=False)
    email = forms.EmailField()
    message = forms.CharField()


class SignUpForm(forms.ModelForm):
    class Meta:
        model = SignUp
        fields = ['full_name', 'email']
        # exclude = ['full_name'] not recommend to use

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_base, provider = email.split('@')
        if not provider == 'gmail.com':
            raise forms.ValidationError('Please use a email address from Gmail mail server.')
        return email

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        # Write validation code.
        return full_name
