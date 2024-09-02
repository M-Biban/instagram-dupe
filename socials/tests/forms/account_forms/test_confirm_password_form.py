"""Unit tests for the Password Confirmation Form"""
from django.test import TestCase
from socials.models import User
from socials.forms import ConfirmPasswordForm

class PasswordFormTestCase(TestCase):
    """Unit tests for the Password Context Processors"""

    fixtures = ['socials/tests/fixtures/default_user.json']

    def setUp(self):
        self.user = User.objects.get(username='johndoe')
        self.form_input = {
            'password': 'Password123',
        }

    def test_form_has_necessary_fields(self):
        form = ConfirmPasswordForm(user=self.user)
        self.assertIn('password', form.fields)

    def test_valid_form(self):
        form = ConfirmPasswordForm(user=self.user, data=self.form_input)
        self.assertTrue(form.is_valid())
        
    def test_invalid_form(self):
        self.form_input['password'] = "WrongPassword123"
        form = ConfirmPasswordForm(user=self.user, data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_must_contain_user(self):
        form = ConfirmPasswordForm(data=self.form_input)
        self.assertFalse(form.is_valid())