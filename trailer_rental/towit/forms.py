from django.forms import ModelForm
from django import forms
from .models import Trailer, UserProfile, Maintenance
from .widgets import BootstrapDateTimePickerInput, BootstrapYearPickerInput
from django.core.files.images import get_image_dimensions

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
    
class MaintenanceForm(ModelForm):
    class Meta:
        model = Maintenance    
        fields = ('date', 'price', 'status', 'comments') 
        
    date = forms.DateField(input_formats=['%d/%m/%Y'],  
        widget=BootstrapDateTimePickerInput(attrs={'placeholder': 'Select a date'}))
    
    
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