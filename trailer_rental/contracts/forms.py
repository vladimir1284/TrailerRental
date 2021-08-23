from django import forms
from .widgets import BootstrapDateTimePickerInput, BootstrapYearPickerInput


# Create the FormContract class
class FormContract(forms.Form):
    # --------- Lesee Info --------
    lessee_name = forms.CharField(
        label='Lessee name *',
        widget=forms.TextInput(attrs={'autofocus': True,
                                      'placeholder': 'Lessee name *'})
    )
    lessee_address = forms.CharField(
        label='Lessee address *',
        widget=forms.TextInput(attrs={'placeholder': 'Lessee address *'})
    )
    lessee_mail = forms.EmailField(
        label='Lessee email *',
        widget=forms.TextInput(attrs={'placeholder': 'Lessee email *'})
    )

    def lessee_info_fields(self):
        return [field for field in self if not field.is_hidden
               and field.name in ('lessee_name', 'lessee_address', 'lessee_mail')]

    # --------- Equipment Description --------
    location = forms.CharField(
        label='Location *',
        widget=forms.TextInput(attrs={'autofocus': True,
                                      'placeholder': 'Location *'})
    )
    model = forms.CharField(
        label='Model *',
        widget=forms.TextInput(attrs={'autofocus': True,
                                      'placeholder': 'Model *'})
    )
    vin = forms.CharField(
        label='VIN *',
        widget=forms.TextInput(attrs={'autofocus': True,
                                      'placeholder': 'VIN *'})
    )
    year = forms.DateTimeField(
        label='Year of manufacture *',
        input_formats=['%Y'], 
        widget=BootstrapYearPickerInput(attrs={'placeholder': 'Year *'})
    )
    length = forms.IntegerField(
        label='Length (in) *',
         widget=forms.TextInput(attrs={'type':'number',
                                      'placeholder': 'Length (in) *'})
    )
    width = forms.IntegerField(
        label='Width (in) *',
         widget=forms.TextInput(attrs={'type':'number',
                                      'placeholder': 'Width (in) *'})
    )
    axles = forms.IntegerField(
        label='Axles quantity *',
         widget=forms.TextInput(attrs={'type':'number',
                                      'placeholder': 'Axles quantity *'})
    )
    color = forms.CharField(
        label='Color *',
        widget=forms.TextInput(attrs={'autofocus': True,
                                      'placeholder': 'Color *'})
    )

    def equipment_description_fields(self):
        return [field for field in self if not field.is_hidden
               and field.name in ('vin', 'model',  'year', 'length',
                                'width', 'axles', 'color','location')]

    # --------- Equipment Inspection --------
    inspection_date = forms.DateTimeField(
        label='Inspection date *',
        input_formats=['%d/%m/%Y'], 
        widget=BootstrapDateTimePickerInput(attrs={'placeholder': 'Inspection date *'})
    )
    current_condition = forms.ChoiceField(
        label='Current trailer condition *',
        choices = ((1,'New'),
                    (2,'Like new'),
                    (3,'Used'))
    )
    bed_type = forms.ChoiceField(
        label='Bed type *',
        choices = ((1,'Wood'),
                    (2,'Steel'))
    )
    bed_comments = forms.CharField(
        label='Coments on bed condition',
        required=False,
        widget=forms.TextInput(attrs={'autofocus': True,
                                      'placeholder': 'Coments on bed condition...'})
    )
    current_tires_condition = forms.ChoiceField(
        label='Current tires condition *',
        choices = ((1,'100%'),
                    (2,'75%'),
                    (3,'50%'))
    )
    spare_tire = forms.ChoiceField(
        label='Does the trailer has spare tire? *',
        choices = ((1,'Yes'),
                    (3,'No'))
    )
    number_of_ramps = forms.IntegerField(
        label='Number of ramps *',
         widget=forms.TextInput(attrs={'type':'number',
                                      'placeholder': 'Number of ramps *'})
    )
    ramps_material= forms.ChoiceField(
        label='Ramps material *',
        choices = ((1,'Aluminium'),
                    (2,'Steel'))
    )
    ramps_comments = forms.CharField(
        label='Coments on ramps condition',
        required=False,
        widget=forms.TextInput(attrs={'autofocus': True,
                                      'placeholder': 'Coments on ramps condition...'})
    )
    electrical_instalation = forms.CharField(
        label='Coments on electrical wired installation',
        required=False,
        widget=forms.TextInput(attrs={'autofocus': True,
                                      'placeholder': 'Coments on electrical wired installation...'})
    )

    def equipment_inspection_fields(self):
        return [field for field in self if not field.is_hidden
               and field.name in ('inspection_date', 'current_condition', 'bed_type',
               'bed_comments','current_tires_condition', 'spare_tire', 'number_of_ramps',
               'ramps_material', 'ramps_comments', 'electrical_instalation')]


    # --------- Contract Terms --------
    effective_date = forms.DateTimeField(
        label='Effective date *',
        input_formats=['%d/%m/%Y'], 
        widget=BootstrapDateTimePickerInput(attrs={'placeholder': 'Effective date *'})
    )
    contract_end_date = forms.DateTimeField(
        label='Contract end date *',
        input_formats=['%d/%m/%Y'], 
        widget=BootstrapDateTimePickerInput(attrs={'placeholder': 'Contract end date *'})
    )
    number_of_payments = forms.IntegerField(
        label='Number of payments *',
         widget=forms.TextInput(attrs={'type':'number',
                                      'placeholder': 'Number of payments *'})
    )
    payment_amount = forms.IntegerField(
        label='Payment amount *',
         widget=forms.TextInput(attrs={'type':'number',
                                      'placeholder': 'Payment amount *'})
    )
    service_charge = forms.IntegerField(
        label='Service charge *',
         widget=forms.TextInput(attrs={'type':'number',
                                      'placeholder': 'Service charge *'})
    )
    security_deposit = forms.IntegerField(
        label='Security deposit *',
         widget=forms.TextInput(attrs={'type':'number',
                                      'placeholder': 'Security deposit *'})
    )
    def contract_terms_fields(self):
        return [field for field in self if not field.is_hidden
               and field.name in ('effective_date', 'contract_end_date', 
                                  'number_of_payments', 'payment_amount',
                                  'service_charge', 'security_deposit')]