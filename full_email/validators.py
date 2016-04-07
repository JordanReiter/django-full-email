import re

from django.core.validators import email_re, EmailValidator, ValidationError
from django.utils.translation import ugettext_lazy as _


EMAIL_REGEX = r'''^(?:['"]?[^@<]+['"]?\s+)?<?(?P<email>[^>]+)>?$'''
class FullEmailValidator(EmailValidator):
    def __call__(self, value):
        try:
            super(FullEmailValidator, self).__call__(value)
        except ValidationError as err:
            # Trivial case failed. Try for possible Full Name <email@address>
            email_match = re.match(EMAIL_REGEX, value or '')
            email_value = None
            if email_match:
                email_value = email_match.groupdict()['email']
            if email_value:
                super(EmailValidator, self).__call__(email_value)
            else:
                raise


validate_full_email = FullEmailValidator(email_re,
                                         _(u'Enter a valid e-mail address.'),
                                         'invalid')
