from django.db import models
from . import formfields
from .validators import validate_full_email


class FullEmailField(models.EmailField):
    default_validators = [validate_full_email]

    def formfield(self, **kwargs):
        defaults = {'form_class': formfields.FullEmailField}
        defaults.update(kwargs)
        return super(FullEmailField, self).formfield(**defaults)
