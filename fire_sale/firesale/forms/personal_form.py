from django.forms import ModelForm, widgets
from django import forms
from firesale.models import PersonalInformation


class PersonalForm(ModelForm):
    auth_user_id = forms.IntegerField()
    class Meta:
        model = PersonalInformation
        exclude = [ 'id', 'auth_user_id', 'user_image_id' ]
        widgets = {
            'name': widgets.TextInput(attrs={'class': 'form-control'}),
            #'seller': widgets.TextInput(attrs={'class': 'form-control'}),
            'bio': widgets.TextInput(attrs={'class': 'form-control'}),
            #'user_image_id': widgets.TextInput(attrs={'class': 'form-control'}),
        }
