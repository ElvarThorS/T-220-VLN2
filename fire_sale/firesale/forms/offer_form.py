from django.forms import ModelForm, widgets
from firesale.models import Offer, Item
from django.contrib.auth import models as auth_models
from django import forms


class OfferForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(OfferForm, self).__init__(*args, **kwargs)
        self.fields['item'] = forms.ModelChoiceField(queryset=Item.objects,required=False, widget=forms.HiddenInput())
        self.fields['is_accepted'] = forms.BooleanField(required=False, widget=forms.HiddenInput())
        self.fields['user_offering'] = forms.ModelChoiceField(queryset=auth_models.User.objects,required=False, widget=forms.HiddenInput())
    class Meta:
        model = Offer
        exclude = ['id']
        widgets = {
            'price': widgets.TextInput(attrs={'class': 'form-control'})
        }
