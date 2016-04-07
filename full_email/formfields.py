from django import forms

from .validators import validate_full_email


class FullEmailField(forms.EmailField):
    default_validators = [validate_full_email]
