"""Unit tests for the Sign Up Form."""
from django.test import TestCase
from socials.models import User
from socials.forms import SignUpForm
from django import forms

class SignUpFormTestCase(TestCase):
    """Unit tests for the Sign Up Form."""

    fixtures = [
        'socials/tests/fixtures/default_user.json',
        'socials/tests/fixtures/other_users.json'
    ]
    
    def setUp(self):
        self.user = User.objects.get(username='johndoe')
        self.other = User.objects.get(username = 'janedoe')
        self.form_input = {
            'first_name': 'Michael',
            'last_name': 'Afton',
            'username': 'PurpleFreak',
            'email' : 'mike@fnaf.com',
            'new_password': 'Password123',
            'password_confirmation': 'Password123'
        }

    def test_form_contains_required_fields(self):
        form = SignUpForm()
        self.assertIn('username', form.fields)
        self.assertIn('new_password', form.fields)
        self.assertIn('first_name', form.fields)
        self.assertIn('last_name', form.fields)
        self.assertIn('email', form.fields)
        password_field = form.fields['new_password']
        self.assertTrue(isinstance(password_field.widget,forms.PasswordInput))
        password_confirmation_field = form.fields['password_confirmation']
        self.assertTrue(isinstance(password_confirmation_field.widget,forms.PasswordInput))

    def test_form_accepts_valid_input(self):
        form = SignUpForm(data=self.form_input)
        self.assertTrue(form.is_valid())
        
    def test_passwords_must_match(self):
        self.form_input['password_confirmation'] = 'WrongPassword123'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        
    def test_new_user_is_created(self):
        form = SignUpForm(data=self.form_input)
        before_count = User.objects.count()
        user = form.save()
        after_count = User.objects.count()
        self.assertEquals(before_count + 1, after_count)
        
    def test_not_unique_username_does_not_create_a_new_user(self):
        self.form_input['username']='johndoe'
        form = SignUpForm(data=self.form_input)
        before_count = User.objects.count()
        self.assertFalse(form.is_valid())
        after_count = User.objects.count()
        self.assertEquals(before_count, after_count)
        
    def test_pasword_must_be_complicated(self):
        self.form_input['new_password']='boring'
        self.form_input['password_confirmation']='boring'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        
