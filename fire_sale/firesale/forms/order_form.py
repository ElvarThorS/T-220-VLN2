from django.forms import ModelForm, widgets
from django import forms
from firesale.models import Order

class OrderForm(ModelForm):
    class Meta:
        model = Order
        exclude = [ 'id' ]
        widgets = {
            'item': None,
            'buyer': None,
            'rate': None,
        }
