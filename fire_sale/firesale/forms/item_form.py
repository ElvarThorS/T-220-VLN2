from django.forms import ModelForm, widgets
from django import forms
from firesale.models import Item


class CreateItemForm(ModelForm):
    image = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter image URL'}))

    class Meta:
        model = Item
        exclude = ['id', 'seller']
        widgets = {
            'name': widgets.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter name'}),
            'condition': widgets.Select(attrs={'class': 'form-control', 'value': 'Select condition'}),
            'description': widgets.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter description'})
        }
