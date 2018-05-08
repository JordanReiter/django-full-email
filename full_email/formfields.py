from django import forms

from .validators import validate_full_email


class FullEmailInput(forms.widgets.TextInput):
    type="text"

    def __init__(self, *args, **kwargs):
        attrs = kwargs.pop('attrs', {})
        attrs['pattern'] = r'^.*<?[^\s@]+@(?:[-\w]+.)+\.\w+>?$'
        kwargs['attrs'] = attrs
        super(FullEmailInput, self).__init__(*args, **kwargs)


class FullEmailField(forms.EmailField):
    widget = FullEmailInput
    default_validators = [validate_full_email]
