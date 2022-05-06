from django.forms import ModelForm, widgets
from django import forms
from firesale.models import Item


class ItemForm(ModelForm):
    image = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model = Item
        exclude = [ 'id', 'seller' ]
        widgets = {
            'name': widgets.TextInput(attrs={'class': 'form-control'}),
            #'seller': widgets.TextInput(attrs={'class': 'form-control'}),
            'description': widgets.TextInput(attrs={'class': 'form-control'}),
            'condition': widgets.TextInput(attrs={'class': 'form-control'}),
        }
