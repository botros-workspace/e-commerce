from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

PAYMENT_CHOICES = (
    ('S','Stripe'),
    ('P','PayPal')
)

class CheckOutForm(forms.Form):
    street_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Sebastianplatz', 
        'class': 'md-form mb-1'
    }))
    building_number = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': '5/1/6',
        'class': 'md-form mb-1'
    }))
    country = CountryField(blank_label='(select country)').formfield(widget = CountrySelectWidget(attrs={
        'class':'custom-select d-block w-100'
    }))
    zip = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    same_shipping_address = forms.BooleanField(required =False)
    save_information = forms.BooleanField(required =False)
    payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices= PAYMENT_CHOICES)
