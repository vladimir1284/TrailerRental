from django.forms import ModelForm
from django import forms
from .models import Trailer
from .widgets import BootstrapDateTimePickerInput, BootstrapYearPickerInput

class TrailerForm(ModelForm):
    class Meta:
        model = Trailer    
        fields = ('name', 'type', 'vin', 'model', 'year', 'length', 'width', 
              'number_of_axles', 'color', 'pictures', 'status', 'location', 'bed_type', 
              'bed_comments', 'has_spare_tire', 'number_of_ramps', 
              'ramps_material', 'ramps_comments', 'electrical_instalation', 
              'price', 'tax_price', 'owner', 'Legal_owner', 'plate', 
              'title', 'title_file', 'title_note', 'sticker', 
              'sticker_file', 'sticker_note') 
        
    year = forms.DateField(input_formats=['%Y',],  
        widget=BootstrapYearPickerInput(attrs={'placeholder': 'Select a year'}))
    pictures = forms.FileField(required=False,
                               widget=forms.ClearableFileInput(attrs={'multiple':True}))