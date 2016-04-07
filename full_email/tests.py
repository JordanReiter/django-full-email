# -*- encoding: utf-8 -*-

from unittest import TestCase
from nose.tools import raises

from django.core.validators import email_re, EmailValidator, ValidationError

from . import validators
from .models import FullEmailField
from .formfields import FullEmailField as FullEmailFormField

from django.db import models
from django import forms

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = FullEmailField()

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email']


class ValidateFullEmail_Tests(TestCase):

    def test_normal_valid_email(self):
        """A normal valid e-mail address validates correctly"""
        validators.validate_full_email(u'john@doe.com')

    def test_fullname(self):
        """A valid e-mail address with a full name validates correctly"""
        validators.validate_full_email(u'John Doe <john@doe.com>')

    def test_quoted_fullname(self):
        """A valid e-mail address with a quoted full name validates correctly"""
        validators.validate_full_email(u'"Doe, John" <john@doe.com>')

    def test_unicode_fullname(self):
        """A valid e-mail address with a Unicode name validates correctly"""
        validators.validate_full_email(u'"Übergeek, Jörg" <joerg@ubergeek.com>')

    @raises(ValidationError)
    def test_incomplete_domain(self):
        """An incomplete domain in an e-mail address fails validation"""
        validators.validate_full_email(u'joerg@ubergeek')

    @raises(ValidationError)
    def test_fullname_and_incomplete_domain(self):
        """An incomplete domain in a full e-mail address fails validation"""
        validators.validate_full_email(u'Jörg <joerg@ubergeek>')

    def test_create_record(self):
        name = 'Person'
        email = '"FirstName LastName" <user@example.com>'
        record = Contact.objects.create(name=name, email=email)
        created = Contact.objects.get(pk=record.pk)
        self.assertEqual(email, created.email)

    def test_normal_form_email(self):
        form = ContactForm({'name': "John", 'email': u'john@doe.com'})
        self.assertEqual(form.is_valid(), True)

    def test_form_valid_email_invalid_name(self):
        form = ContactForm({'email': u'john@doe.com'})
        self.assertEqual(form.is_valid(), False)
        self.assertNotIn('email', form.errors)

    def test_fullname(self):
        """A valid e-mail address with a full name validates correctly"""
        form = ContactForm({'name': "John", 'email': u'John Doe <john@doe.com>'})
        self.assertEqual(form.is_valid(), True)

    def test_quoted_fullname(self):
        """A valid e-mail address with a quoted full name validates correctly"""
        form = ContactForm({'name': "John", 'email': u'"Doe, John" <john@doe.com>'})
        self.assertEqual(form.is_valid(), True)

    def test_unicode_fullname(self):
        """A valid e-mail address with a Unicode name validates correctly"""
        form = ContactForm({'name': "John", 'email': u'"Übergeek, Jörg" <joerg@ubergeek.com>'})
        self.assertEqual(form.is_valid(), True)

    def test_incomplete_domain(self):
        """An incomplete domain in an e-mail address fails validation"""
        form = ContactForm({'name': "John", 'email': u'joerg@ubergeek'})
        self.assertEqual(form.is_valid(), False)
        self.assertIn('email', form.errors)

    def test_fullname_and_incomplete_domain(self):
        """An incomplete domain in a full e-mail address fails validation"""
        form = ContactForm({'name': "John", 'email': u'Jörg <joerg@ubergeek>'})
        self.assertEqual(form.is_valid(), False)
        self.assertIn('email', form.errors)

    def test_correct_formfield(self):
        form = ContactForm()
        self.assertIsInstance(form.fields['email'], FullEmailFormField)
