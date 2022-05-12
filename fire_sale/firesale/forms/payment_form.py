from django.forms import ModelForm, DateInput, widgets
from firesale.models import Payment

class PaymentForm(ModelForm):

    class Meta:
        model = Payment
        exclude = ['id']
        widgets = {
            'card_holder_name': widgets.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter cardholder name'}),
            'card_number': widgets.TextInput(attrs={'class': 'form-control', 'placeholder': 'xxxx-xxxx-xxxx-xxxx'}),
            'expiration_date': DateInput(attrs={'class':'form-control', 'placeholder': 'Enter expiration date'}),
            'cvc': widgets.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter CVC'}),
        }
