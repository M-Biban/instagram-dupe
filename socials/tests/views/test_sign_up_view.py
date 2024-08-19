"""Unit tests for the SignUpView."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from socials.models import User
from django.urls import reverse
from socials.forms import SignUpForm

class SignUpViewTestCase(TestCase):
    """Unit tests for Sign Up View."""

    fixtures = [
        'socials/tests/fixtures/default_user.json',
        'socials/tests/fixtures/other_users.json'
    ]
    
    def setUp(self):
        self.url = reverse('sign-up')
        self.user = User.objects.get(username='johndoe')
        self.form_input = {
            'first_name': 'Michael',
            'last_name': 'Afton',
            'username': 'PurpleFreak',
            'email' : 'mike@fnaf.com',
            'new_password': 'Password123',
            'password_confirmation': 'Password123'
        }
        
    def test_sign_up_url(self):
        self.assertEquals(self.url, '/sign-up/')
        
    def test_get_sign_up(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sign-up.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, SignUpForm))
        self.assertFalse(form.is_bound)
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)
        
    def test_valid_form_input_creates_new_user(self):
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        after_count = User.objects.count()
        self.assertEquals(before_count + 1, after_count)
        response_url = reverse('dashboard')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        
    def test_blank_password(self):
        before_count = User.objects.count()
        self.form_input['new_password'] = ''
        self.form_input['password_confirmation'] = ''
        response = self.client.post(self.url, self.form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        after_count = User.objects.count()
        self.assertEquals(before_count, after_count)