from django.forms import ModelForm, widgets
from firesale.models import User


class UserEditForm(ModelForm):
    class Meta:
        model = User
        exclude = ['id', 'password', 'last_login', 'is_superuser', 'username', 'is_staff', 'is_active', 'date_joined']
        widgets = {
            'first_name': widgets.TextInput(attrs={'class': 'form-control'})
        }