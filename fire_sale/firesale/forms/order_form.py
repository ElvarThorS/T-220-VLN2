from django.forms import ModelForm, widgets
from django import forms
from firesale.models import Order

class OrderForm(ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', '')
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['item'].widget = forms.HiddenInput()
        self.fields['buyer'].widget = forms.HiddenInput()
        self.fields['price'].widget = forms.HiddenInput()
        self.fields['rating'].label = "Rate the seller:"
    class Meta:
        model = Order
        exclude = ['id']
        widgets = {
            'item': widgets.TextInput(attrs={'class': 'form-control'}),
            'buyer': widgets.TextInput(attrs={'class': 'form-control'}),
            'rating': widgets.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Range: 1-5'}),
        }
