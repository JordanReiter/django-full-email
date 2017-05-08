import re

from django.core.validators import EmailValidator, ValidationError
from django.utils.translation import ugettext_lazy as _


EMAIL_REGEX = r'''^(?:['"]?[^@<]+['"]?\s+)?<?(?P<email>[^>]+)>?$'''
class FullEmailValidator(EmailValidator):
    def __call__(self, value):
        try:
            EmailValidator.__call__(self, value)
        except ValidationError as err:
            # Trivial case failed. Try for possible Full Name <email@address>
            email_match = re.match(EMAIL_REGEX, value or '')
            email_value = None
            if email_match:
                email_value = email_match.groupdict()['email']
            if email_value:
                EmailValidator.__call__(self, email_value)
            else:
                raise


validate_full_email = FullEmailValidator()
