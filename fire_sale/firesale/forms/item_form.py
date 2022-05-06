from django.contrib.auth.models import User
from django.forms import ModelForm, widgets
from django import forms
from firesale.models import Item



class CreateItemForm(ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', '')
        super(CreateItemForm, self).__init__(*args, **kwargs)
        self.fields['seller'] = forms.ModelChoiceField(queryset=User.objects,required=False, widget=forms.HiddenInput())

    image = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control'}))
    #seller = forms.ModelChoiceField(queryset=User.objects.filter(),required=False, widget=forms.HiddenInput())
    class Meta:
        model = Item
        exclude = [ 'id' ]
        widgets = {
            'name': widgets.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter name'}),
            'condition': widgets.Select(attrs={'class': 'form-control', 'value': 'Select condition'}),
            'description': widgets.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter description'}),

        }
