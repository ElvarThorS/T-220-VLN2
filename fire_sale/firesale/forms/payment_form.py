from django.forms import ModelForm, DateInput, widgets, DateField
from firesale.models import Payment

class PaymentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Payment
        exclude = ['id']
        widgets = {
            'card_holder_name': widgets.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter cardholder name'}),
            'card_number': widgets.TextInput(attrs={'class': 'form-control', 'placeholder': 'xxxx-xxxx-xxxx-xxxx'}),
            'expiration_date': DateInput(),
            'cvc': widgets.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter CVC'}),
        }
