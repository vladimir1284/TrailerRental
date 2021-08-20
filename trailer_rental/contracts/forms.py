from django import forms
from .widgets import BootstrapDateTimePickerInput


# Create the FormContract class
class FormContract(forms.Form):
    lessee_name = forms.CharField(
        label='lessee_info',
        widget=forms.TextInput(attrs={'autofocus': True,
                                      'placeholder': 'Lessee name *'})
    )
    lessee_address = forms.CharField(
        label='lessee_info',
        widget=forms.TextInput(attrs={'placeholder': 'Lessee address *'})
    )
    lessee_mail = forms.EmailField(
        label='lessee_info',
        widget=forms.TextInput(attrs={'placeholder': 'Lessee email *'})
    )
    location = forms.CharField(
        label='equipment_description',
        widget=forms.TextInput(attrs={'autofocus': True,
                                      'placeholder': 'Location *'})
    )
    model = forms.CharField(
        label='equipment_description',
        widget=forms.TextInput(attrs={'autofocus': True,
                                      'placeholder': 'Model *'})
    )
    vin = forms.CharField(
        label='equipment_description',
        widget=forms.TextInput(attrs={'autofocus': True,
                                      'placeholder': 'VIN *'})
    )
    effective_date = forms.DateTimeField(
        label='contract_terms',
        input_formats=['%d/%m/%Y'], 
        widget=BootstrapDateTimePickerInput(attrs={'placeholder': 'Effective date *'})
    )
    contract_end_date = forms.DateTimeField(
        label='contract_terms',
        input_formats=['%d/%m/%Y'], 
        widget=BootstrapDateTimePickerInput(attrs={'placeholder': 'Contract end date *'})
    )
    number_of_payments = forms.IntegerField(
        label='contract_terms',
         widget=forms.TextInput(attrs={'type':'number',
                                      'placeholder': 'Number of payments *'})
    )
    payment_amount = forms.IntegerField(
        label='contract_terms',
         widget=forms.TextInput(attrs={'type':'number',
                                      'placeholder': 'Payment amount *'})
    )
    service_charge = forms.IntegerField(
        label='contract_terms',
         widget=forms.TextInput(attrs={'type':'number',
                                      'placeholder': 'Service charge *'})
    )
    security_deposit = forms.IntegerField(
        label='contract_terms',
         widget=forms.TextInput(attrs={'type':'number',
                                      'placeholder': 'Security deposit *'})
    )