from django import forms

class ContactForm(forms.Form):
    full_name = forms.CharField(label="Full name", max_length=255)
    street_name = forms.CharField(label="Street Name", max_length=255)
    house_number = forms.IntegerField(label="House Number")
    country = forms.CharField(label="Country", max_length=255)
    postal_code = forms.IntegerField(label="Postal Code")
