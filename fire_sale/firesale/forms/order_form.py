from django.forms import ModelForm, widgets
from django import forms
from firesale.models import Order

class OrderForm(ModelForm):
    class Meta:
        model = Order
        exclude = [ 'id' ]
        widgets = {
            'item': widgets.TextInput(attrs={'class': 'form-control'}),
            'buyer': widgets.TextInput(attrs={'class': 'form-control'}),
            'rating': widgets.TextInput(attrs={'class': 'form-control'}),
        }
