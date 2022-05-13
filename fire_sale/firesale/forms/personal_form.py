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

class UpdatePersonalForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(UpdatePersonalForm, self).__init__(*args, **kwargs)
        self.fields['auth_user'].widget = forms.HiddenInput()
        self.fields['country'].widget = forms.HiddenInput()
        self.fields['street_name'].widget = forms.HiddenInput()
        self.fields['house_number'].widget = forms.HiddenInput()
        self.fields['postal_code'].widget = forms.HiddenInput()
        self.fields['payment_info'].widget = forms.HiddenInput()
        self.fields['user_image'].widget = forms.HiddenInput()

    image = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = PersonalInformation
        exclude = ['id', 'auth_user_id']
        widgets = {
            'name': widgets.TextInput(attrs={'class': 'form-control'}),
            'bio': widgets.Textarea(attrs={'class': 'form-control'}),
        }
