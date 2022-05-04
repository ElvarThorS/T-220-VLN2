from django import forms
from .models import User

class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password', 'personal_information', 'user_image')

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.TextInput(attrs={'class': 'form-control'}),
            'personal_information': forms.TextInput(attrs={'class': 'form-control'}),
            'user_image': forms.TextInput(attrs={'class': 'form-control'}),
        }