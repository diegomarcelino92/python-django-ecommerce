from typing import Any

from django import forms
from django.contrib.auth.models import User

from profiles.models import Profile, ProfileAddress


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ('user',)


class ProfileAddressForm(forms.ModelForm):
    class Meta:
        model = ProfileAddress
        fields = '__all__'
        exclude = ('profile',)


class UserForm(forms.ModelForm):
    password = forms.CharField(required=False, widget=forms.PasswordInput())
    password2 = forms.CharField(required=False, widget=forms.PasswordInput(), label='Confirm Password')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password', )

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean(self) -> dict[str, Any]:
        super().clean()
        cleaned_data = self.cleaned_data
        error_messages = {}

        passsword_data = cleaned_data.get('password')
        username_data = cleaned_data.get('username')
        email_data = cleaned_data.get('email')

        username = User.objects.filter(username=username_data).first()
        email = User.objects.filter(email=email_data).first()

        if self.user:
            if passsword_data:
                self.__validate_passoword(error_messages)

        if not self.user:
            self.__validate_passoword(error_messages)

            if username or email:
                error_messages['username'] = 'Username or email already exists'
                error_messages['email'] = 'Username or email already exists'

        if error_messages:
            raise forms.ValidationError(error_messages)

    def __validate_passoword(self, messages):
        cleaned_data = self.cleaned_data

        passsword_data = cleaned_data.get('password')
        passsword2_data = cleaned_data.get('password2')

        if len(passsword_data) < 8:
            messages['password'] = 'Password must be at least 8 characters'

        if passsword_data != passsword2_data:
            messages['password2'] = 'Passwords do not match'
