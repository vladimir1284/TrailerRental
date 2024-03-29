from django.forms import ModelForm
from towit.models import *
from towit.model.tracker import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div, HTML
from crispy_forms.bootstrap import PrependedText, AppendedText
from towit.models import Status


class TrackerLesseeForm(ModelForm):
    class Meta:
        model = Tracker
        fields = ('lessee_name',)


class TrackerForm(ModelForm):
    class Meta:
        model = Tracker
        fields = ('owner', 'imei',  'device_password',  'device_id', 'traccar_url', 'feed_traccar',
                  'phone_password', 'Tcheck', 'Mode', 'Tint', 'TintB',
                  'TGPS', 'TGPSB', 'SMART', 'Tsend', 'TsendB', 'trailer_description',
                  'trailer_bin_number', 'lessee_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['feed_traccar'].label = "Active"
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Tracker device',
                Div(
                    Div(
                        'imei',
                        css_class='col-6'
                    ),
                    Div(
                        'device_password',
                        css_class='col-6'
                    ),
                    css_class='row'
                )
            ),
            Fieldset(
                'SIM',
                Div(
                    Div(
                        'device_id',
                        css_class='col-6'
                    ),
                    Div(
                        'phone_password',
                        css_class='col-6'
                    ),
                    css_class='row'
                ),
                'owner',
            ),
            Fieldset(
                'Traccar',
                Div(
                    Div(
                        'traccar_url',
                        css_class='col-10'
                    ),
                    Div(
                        'feed_traccar',
                        css_class='col-2'
                    ),
                    css_class='row'
                )
            ),
            Fieldset(
                'General',
                Div(
                    Div(
                        'Mode',
                        css_class='col-4'
                    ),
                    Div(
                        'SMART',
                        css_class='col-4'
                    ),
                    Div(
                        AppendedText('Tcheck', "min"),
                        css_class='col-4'
                    ),
                    css_class='row'
                )
            ),
            Fieldset(
                'Powered times',
                Div(
                    Div(
                        AppendedText('Tint', "min"),
                        css_class='col-4'
                    ),
                    Div(
                        AppendedText('Tsend', "min"),
                        css_class='col-4'
                    ),
                    Div(
                        AppendedText('TGPS', "min"),
                        css_class='col-4'
                    ),
                    css_class='row'
                )
            ),
            Fieldset(
                'Battery times',
                Div(
                    AppendedText('TintB', "min"),
                    css_class='col-4'
                )
            ),
            Fieldset(
                'Trailer data',
                Div(
                    AppendedText('TsendB', "min"),
                    css_class='col-4'
                ),
                Div(
                    AppendedText('TGPSB', "min"),
                    css_class='col-4'
                ),
                css_class='row'
            ),
            Fieldset(
                'Trailer data',
                Div(
                    'trailer_description',
                    css_class='col-12'
                ),
                Div(
                    'trailer_bin_number',
                    css_class='col-12'
                ),
                Div(
                    'lessee_name',
                    css_class='col-12'
                )
            ),
            ButtonHolder(
                Submit('submit', 'Register tracker',
                       css_class='btn btn-success')
            )

        )
