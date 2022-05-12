from django.forms import ModelForm, DateInput
from firesale.models import Payment

class PaymentForm(ModelForm):

    class Meta:
        model = Payment
        exclude = ['id']
        widgets = {
            'card_holder_name': widgets.TextInput(attrs={'class': 'form-control'}),
            'card_number': widgets.TextInput(attrs={'class': 'form-control'}),
            'expiration_date': DateInput(attrs='class':'form-control'),
            'cvc': widgets.TextInput(attrs={'class': 'form-control'}),
        }
