from typing import Any
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    UserChangeForm, 
    UserCreationForm
)

from .models import Profile

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model =User
        fields = ('email', 'is_superuser')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'is_superuser')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'image',
            'profession',
            'mobile_number'
        )

    def clean_mobile_number(self) -> str:
        mobile_number = self.cleaned_data.get('mobile_number', '')
        if mobile_number and not mobile_number.isdigit():
            raise forms.ValidationError('Only numeric values are allowed.')
        if mobile_number and len(mobile_number) < 10:
            raise forms.ValidationError('Mobile number must be at least 10 characters')
        return mobile_number
    
    def clean_profession(self):
        profession = self.cleaned_data.get('profession', '')
        if profession and len(profession) < 5:
            raise forms.ValidationError('Profession must be at least 5 characters')
        return profession