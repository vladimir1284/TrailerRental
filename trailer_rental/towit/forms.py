from django.forms import ModelForm
from django import forms
from .models import Trailer, UserProfile, Maintenance, Contact, Lessee, Lease, HandWriting
from .widgets import BootstrapDateTimePickerInput, BootstrapYearPickerInput
from django.core.files.images import get_image_dimensions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div, HTML
from crispy_forms.bootstrap import PrependedText, AppendedText
from towit.models import Status

class TrailerForm(ModelForm):
    class Meta:
        model = Trailer    
        fields = ('name', 'type', 'vin', 'year', 'size', 'current_tires_condition',
              'number_of_axles', 'color', 'pictures', 'status', 'bed_type', 
              'bed_comments', 'has_spare_tire', 'number_of_ramps', 'plate_stage',
              'ramps_material', 'ramps_length', 'electrical_instalation', 
              'price', 'tax_price', 'owner', 'Legal_owner', 'plate', 
              'title', 'title_file', 'title_note', 'sticker', 
              'sticker_file', 'sticker_note') 
        
    year = forms.DateField(input_formats=['%Y',],  
        widget=BootstrapYearPickerInput())
    pictures = forms.FileField(required=False,
                               widget=forms.ClearableFileInput(attrs={'multiple':True}))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Specifications',
                Div(
                    Div(
                        'name',
                        css_class = 'col-6'
                    ),
                    Div(
                        'vin',
                        css_class = 'col-6'
                    ),
                    css_class = 'row'
                ),
                Div(
                    Div(
                        'type',
                        css_class = 'col-4'
                    ),
                    Div(
                        'color',
                        css_class = 'col-4'
                    ),
                    Div(
                        AppendedText('size', "'"),
                        css_class = 'col-4'
                    ),
                    css_class = 'row'
                ),
                Div(
                    Div(
                        'number_of_axles',
                        css_class = 'col-4'
                    ),
                    Div(
                        'status',
                        css_class = 'col-4'
                    ),
                    Div(
                        'year',
                        css_class = 'col-4'
                    ),
                    css_class = 'row'
                ),
                Div(
                    Div(
                        'current_tires_condition',
                        css_class = 'col-6'
                    ),
                    Div(
                        'has_spare_tire',
                        css_class = 'col-6'
                    ),
                    css_class = 'row'
                ),
                Div(
                    Div(
                        'number_of_ramps',
                        css_class = 'col-4'
                    ),
                    Div(
                        'ramps_material',
                        css_class = 'col-4'
                    ),
                    Div(
                        'ramps_length',
                        css_class = 'col-4'
                    ),
                    css_class = 'row'
                ),
                Div(
                    Div(
                        'bed_type',
                        css_class = 'col-6'
                    ),
                    Div(
                        'pictures',
                        css_class = 'col-6'
                    ),
                    css_class = 'row'
                ),
                'bed_comments',
                'electrical_instalation'
            ),
            Fieldset(
                'Legal matters',
                Div(
                    Div(
                        'owner',
                        css_class = 'col-6'
                    ),
                    Div(
                        'Legal_owner',
                        css_class = 'col-6'
                    ),
                    css_class = 'row'
                ),
                Div(
                    Div(
                        PrependedText('price', '$'),
                        css_class = 'col-6'
                    ),
                    Div(
                        PrependedText('tax_price', '$'),
                        css_class = 'col-6'
                    ),
                    css_class = 'row'
                ),
                Div(
                    Div(
                        'plate',
                        css_class = 'col-6'
                    ),
                    Div(
                        'plate_stage',
                        css_class = 'col-6'
                    ),
                    css_class = 'row'
                ),
                Div(
                    Div(
                        Div(
                            Div(
                                'title',
                                css_class = 'col-4'
                            ),
                            Div(
                                'title_file',
                                css_class = 'col-8'
                            ),
                            css_class = 'card-header row' 
                        ),
                        Div(
                            'title_note',
                            css_class = 'card-body col-12'
                        ),
                        css_class = 'row card'
                    )
                )
            ),
            Div(
                Div(
                    Div(
                        Div(
                            'sticker',
                            css_class = 'col-4'
                        ),
                        Div(
                            'sticker_file',
                            css_class = 'col-8'
                        ),
                        css_class = 'card-header row' 
                    ),
                    Div(
                        'sticker_note',
                        css_class = 'card-body col-12'
                    ),
                    css_class = 'row card'
                )
            ),
            ButtonHolder(
                Submit('submit', 'Save trailer', css_class='btn btn-success')
            )
        )
    
    
class MaintenanceForm(ModelForm):
    class Meta:
        model = Maintenance    
        fields = ('date', 'price', 'status', 'comments') 
        
    date = forms.DateField(input_formats=['%d/%m/%Y'],  
        widget=BootstrapDateTimePickerInput(attrs={'placeholder': 'Select a date'}))
    
class HandWritingForm(ModelForm):
    class Meta:
        model = HandWriting    
        fields = ('img', 'position', 'lease') 
        
    img = forms.CharField(max_length=20000)
    
class ContactForm(ModelForm):
    class Meta:
        model = Contact    
        fields = ('name', 'address', 'mail', 'phone', 'interest', 'size', 
                  'price', 'term', 'term_unit','type', 'interest_date') 
        
    interest_date = forms.DateField(input_formats=['%d/%m/%Y'],  
        widget=BootstrapDateTimePickerInput(attrs={'placeholder': 'Select a date'}))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                '',
                'name', 'address', 'mail', 'phone', 
                Div(
                    Div(
                        'term',
                        css_class = 'col-8'
                    ),
                    Div(
                        'term_unit',
                        css_class = 'col-4'
                    ),
                    css_class = 'row'
                ),
                Div(
                    Div(
                        'interest',
                        css_class = 'col-5'
                    ),
                    Div(
                        'interest_date',
                        css_class = 'col-7'
                    ),
                    css_class = 'row'
                ),
                Div(
                    Div(
                        'type',
                        css_class = 'col-4'
                    ),
                    Div(
                        AppendedText('size',"'"),
                        css_class = 'col-3'
                    ),
                    Div(
                        PrependedText('price', '$', placeholder="Price to client"),
                        css_class = 'col-5'
                    ),
                    css_class = 'row'
                )
            ),
            ButtonHolder(
                Submit('submit', 'Save contact', css_class='btn btn-success')
            )
        )
    
class LesseeForm(ModelForm):
    class Meta:
        model = Lessee    
        fields = ('name', 'address', 'mail', 'phone', 'insurance_number', 
                  'insurance_file', 'license_number', 'license_file') 
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                '',
                'name', 'address', 'mail', 'phone', 
                Div(
                    Div(
                        'license_number',
                        css_class = 'col-6'
                    ),
                    Div(
                        'license_file',
                        css_class = 'col-6'
                    ),
                    css_class = 'row'
                ),
                Div(
                    Div(
                        'insurance_number',
                        css_class = 'col-6'
                    ),
                    Div(
                        'insurance_file',
                        css_class = 'col-6'
                    ),
                    css_class = 'row'
                ),
            ButtonHolder(
                Submit('submit', 'Proceed to rent', css_class='btn btn-success')
                )
            )
        )
     
class LeaseForm(ModelForm):
    class Meta:
        model = Lease    
        fields = ('lessee', 'trailer', 'location', 'location_file', 
                  'effective_date', 'contract_end_date', 'number_of_payments', 
                  'payment_amount', 'service_charge', 'security_deposit', 
                  'inspection_date', 'current_condition') 
        
    effective_date = forms.DateField(input_formats=['%d/%m/%Y'],  
        widget=BootstrapDateTimePickerInput(attrs={'placeholder': 'Select a date'}))
        
    contract_end_date = forms.DateField(input_formats=['%d/%m/%Y'],  
        widget=BootstrapDateTimePickerInput(attrs={'placeholder': 'Select a date'}))
        
    inspection_date = forms.DateField(input_formats=['%d/%m/%Y'],  
        widget=BootstrapDateTimePickerInput(attrs={'placeholder': 'Select a date'}))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)        
        
        # Filters
        free_status = Status.objects.filter(name__icontains="free")[0]
        self.fields["trailer"].queryset = Trailer.objects.filter(status=free_status)
        
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Contract terms',
                Div(
                    Div(
                        'lessee',
                        css_class = 'col-6'
                    ),
                    Div(
                        'trailer',
                        css_class = 'col-6'
                    ),
                    css_class = 'row'
                ),
                Div(
                    Div(
                        'location',
                        css_class = 'col-6'
                    ),
                    Div(
                        'location_file',
                        css_class = 'col-6'
                    ),
                    css_class = 'row'
                ),
                Div(
                    Div(
                        'effective_date',
                        css_class = 'col-6'
                    ),
                    Div(
                        'contract_end_date',
                        css_class = 'col-6'
                    ),
                    css_class = 'row'
                ),
                Div(
                    Div(
                        'number_of_payments',
                        css_class = 'col-6'
                    ),
                    Div(
                        PrependedText('payment_amount', '$'),
                        css_class = 'col-6'
                    ),
                    css_class = 'row'
                ),
                Div(
                    Div(
                        PrependedText('service_charge', '$'),
                        css_class = 'col-6'
                    ),
                    Div(
                        PrependedText('security_deposit', '$'),
                        css_class = 'col-6'
                    ),
                    css_class = 'row'
                )
            ),
            Fieldset(
                'Inspection',
                HTML('<div id="id_trailer_conditions" class="col-12"></div>'),
                Div(
                    Div(
                        'current_condition',
                        css_class = 'col-6'
                    ),
                    Div(
                        'inspection_date',
                        css_class = 'col-6'
                    ),
                    css_class = 'row'
                ),
            ButtonHolder(
                Submit('submit', 'Create contract', css_class='btn btn-success')
                )
            )
        )
       
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('avatar',)
                  
    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']

        try:
            w, h = get_image_dimensions(avatar)

            #validate dimensions
            max_width = max_height = 100
            if w > max_width or h > max_height:
                raise forms.ValidationError(
                    u'Please use an image that is '
                     '%s x %s pixels or smaller.' % (max_width, max_height))

            #validate content type
            main, sub = avatar.content_type.split('/')
            if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
                raise forms.ValidationError(u'Please use a JPEG, '
                    'GIF or PNG image.')

            #validate file size
            if len(avatar) > (20 * 1024):
                raise forms.ValidationError(
                    u'Avatar file size may not exceed 20k.')

        except AttributeError:
            """
            Handles case when we are updating the user profile
            and do not supply a new avatar
            """
            pass

        return avatar