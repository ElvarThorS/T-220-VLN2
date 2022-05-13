from django import forms

class ContactForm(forms.Form):
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your full name'}), label="Full name", max_length=255)
    #city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your street name'}), label="Street Name", max_length=255)
    street_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your street name'}), label="Street Name", max_length=255)
    house_number = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter your house number'}), label="House Number")
    country = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your country'}), label="Country", max_length=255)
    postal_code = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter your postal code'}), label="Postal Code")
