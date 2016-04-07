===========================================
 Full e-mail address validation for Django
===========================================

Out of the box, Django e-mail fields for both database models and forms only
accept plain e-mail addresses.  For example, ``joe@hacker.com`` is accepted.

On the other hand, full e-mail addresses which include a human-readable name,
for example the following address fails validation in Django::

    Joe Hacker <joe@hacker.com>

This package adds support for validating full e-mail addresses.

Database model example
======================

::

    from django import models
    from full_email.models import FullEmailField

    class MyModel(models.Model):
        email = FullEmailField()

Forms example
=============

::

    from django import forms
    from full_email.formfields import FullEmailField

    class MyForm(forms.Form):
        email = FullEmailField(label='E-mail address')


Notes from Jordan
=================

Nearly all of the code in this package is based on the work of Antti Kaihola
from the gist published here: https://gist.github.com/akaihola/1505228

Most of my work was just adding the setup.py and adding additional test cases
to make sure that the model field and form field were behaving correctly. Note
that I think the test cases may not work correctly for Django 1.7+ and will need
to be rewritten for forwards compatibility; I was able to find good documentation
on how to do dynamic testing modules in the short tiime I had to write up the tests.

I did make one minor change to the validator, which relies on a regular
expression to extract the email address rather than splitting the string on the 
less-than bracket.
