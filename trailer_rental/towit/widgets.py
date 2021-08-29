from django.forms import DateTimeInput

class BootstrapDateTimePickerInput(DateTimeInput):
    template_name = 'towit/widgets/bootstrap_datetimepicker.html'

    def get_context(self, name, value, attrs):
        datetimepicker_id = 'datetimepicker_{name}'.format(name=name)
        if attrs is None:
            attrs = dict()
        attrs['data-target'] = '#{id}'.format(id=datetimepicker_id)
        attrs['class'] = 'form-control datetimepicker-input'
        context = super().get_context(name, value, attrs)
        context['widget']['datetimepicker_id'] = datetimepicker_id
        context['widget']['name'] = name
        context['widget']['fecha_inicial'] = value
        return context

class BootstrapYearPickerInput(DateTimeInput):
    template_name = 'towit/widgets/bootstrap_yearpicker.html'

    def get_context(self, name, value, attrs):
        yearpicker_id = 'yearpicker_{name}'.format(name=name)
        if attrs is None:
            attrs = dict()
        attrs['data-target'] = '#{id}'.format(id=yearpicker_id)
        attrs['class'] = 'form-control yearpicker-input'
        context = super().get_context(name, value, attrs)
        context['widget']['yearpicker_id'] = yearpicker_id
        context['widget']['name'] = name
        return context