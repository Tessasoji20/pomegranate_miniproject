from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm


ALLOWED_DOMAIN = "@rajagiri.edu.in"


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'})
    )

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if not email.endswith(ALLOWED_DOMAIN):
            raise ValidationError(
                "Only @rajagiri.edu.in email addresses are allowed."
            )

        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")

        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords do not match.")

        return cleaned_data

class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'placeholder': 'Email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )

    def clean_username(self):
        email = self.cleaned_data.get('username')

        if not email.endswith(ALLOWED_DOMAIN):
            raise ValidationError("Only @rajagiri.edu.in email addresses are allowed.")

        # convert email → username
        try:
            user = User.objects.get(email=email)
            return user.username
        except User.DoesNotExist:
            raise ValidationError("No account found with this email.")

    def confirm_login_allowed(self, user):
        if not user.email.endswith(ALLOWED_DOMAIN):
            raise ValidationError(
                "Access restricted to @rajagiri.edu.in users only."
            )