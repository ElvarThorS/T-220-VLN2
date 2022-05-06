from django.forms import ModelForm, widgets
from django import forms
from firesale.models import Item


class CreateItemForm(ModelForm):
    image = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter image URL'}))

    class Meta:
        model = Item
        exclude = ['id', 'seller']
        widgets = {
<<<<<<< HEAD
            'name': widgets.TextInput(attrs={'class': 'form-control'}),
            #'seller': widgets.TextInput(attrs={'class': 'form-control'}),
            'description': widgets.TextInput(attrs={'class': 'form-control'}),
            'condition': widgets.TextInput(attrs={'class': 'form-control'}),
=======
            'name': widgets.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter name'}),
            'condition': widgets.Select(attrs={'class': 'form-control', 'value': 'Select condition'}),
            'description': widgets.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter description'})
>>>>>>> da5e00bd27a9b42cdf6bd608df7941b19192b742
        }
