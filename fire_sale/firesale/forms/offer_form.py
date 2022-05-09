from django.forms import ModelForm, widgets
from firesale.models import Offer


class OfferForm(ModelForm):
    class Meta:
        model = Offer
        exclude = []
        widgets = {
            'first_name': widgets.TextInput(attrs={'class': 'form-control'})
        }
