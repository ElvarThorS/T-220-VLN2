from django.forms import ModelForm, widgets
from django import forms
from firesale.models import Review

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        exclude = [ 'id' ]
        widgets = {
            'item': None,
            'buyer': None,
            'rate': None,
        }
