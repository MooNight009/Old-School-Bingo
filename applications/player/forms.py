from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# TODO: Write clean methods for each part
from applications.player.models import Player


class CreateUserForm(UserCreationForm):
    """
        Create a new user and player
    """

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'})
        }

        help_texts = {
            'username': 'This name is what you will be shown as in the website and is different from your OSRS account names. Letters, digits and @/./+/-/_ only.'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = super().clean()

        if User.objects.filter(email=cleaned_data['email']).exists():
            raise forms.ValidationError({'email': ['An account with the entered email already exists.']})

        return cleaned_data

    def save(self, *args, **kwargs):
        user = super().save(*args, **kwargs)
        user.is_active = False
        user.save()
        player = Player(user=user)
        player.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=32, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('Username or password is wrong. ')
            return super().clean()
        raise forms.ValidationError('Error')


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'required': 'required'}))

    def clean(self):
        cleaned_data = self.cleaned_data
        email = cleaned_data['email']

        user = User.objects.filter(email=email)
        if not user.exists():
            raise forms.ValidationError({'email': ['Email address does not exist!']})
        return cleaned_data


class ResetPasswordForm(forms.Form):
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'class': 'form-control'}),
        # help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'class': 'form-control'}),
        strip=False,
        help_text="Enter the same password as before, for verification.",
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data['password1']

        min_length = 8

        if len(password1) < min_length:
            raise forms.ValidationError({'password1': [f'Password must be at least {min_length} characters long.']})

        # check for digit
        if not any(char.isdigit() for char in password1):
            raise forms.ValidationError({'password1': ['Password must contain at least 1 digit.']})

        # check for letter
        if not any(char.isalpha() for char in password1):
            raise forms.ValidationError({'password1': ['Password must contain at least 1 letter.']})

        if cleaned_data['password1'] != cleaned_data['password2']:
            raise forms.ValidationError({'password2': ['The two password fields didn’t match']})

        return cleaned_data
