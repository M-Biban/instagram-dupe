"""Unit tests for the Log In Form."""
from django.test import TestCase
from socials.models import User
from socials.forms import LogInForm
from django import forms

class LogInFormTestCase(TestCase):
    """Unit tests for the Log In Form."""

    fixtures = [
        'socials/tests/fixtures/default_user.json',
        'socials/tests/fixtures/other_users.json'
    ]
    
    def setUp(self):
        self.user = User.objects.get(username='johndoe')
        self.other = User.objects.get(username = 'janedoe')
        self.form_input = {'username': 'johndoe', 'password': 'Password123'}

    def test_form_contains_required_fields(self):
        form = LogInForm()
        self.assertIn('username', form.fields)
        self.assertIn('password', form.fields)
        password_field = form.fields['password']
        self.assertTrue(isinstance(password_field.widget,forms.PasswordInput))

    def test_form_accepts_valid_input(self):
        form = LogInForm(data=self.form_input)
        self.assertTrue(form.is_valid())
        
    def test_form_accepts_wrong_username(self):
        self.form_input['username'] = 'john'
        form = LogInForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        
    def test_form_accepts_wrong_password(self):
        self.form_input['password'] = 'john'
        form = LogInForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        
    def test_form_authenticates_user(self):
        form = LogInForm(data=self.form_input)
        user = form.get_user()
        self.assertEqual(user, self.user)
        
    def test_invalid_form(self):
        self.form_input['username']= ''
        form = LogInForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertNotEqual(self.user, form.get_user())