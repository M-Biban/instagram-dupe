"""Unit tests for the LogInView."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from socials.models import User
from django.urls import reverse
from socials.forms import LogInForm
from socials.views import LogInView, LoginProhibitedMixin
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings

class LogInViewTestCase(TestCase):
    """Unit tests for Sign Up View."""

    fixtures = [
        'socials/tests/fixtures/default_user.json',
        'socials/tests/fixtures/other_users.json'
    ]
    
    def setUp(self):
        self.url = reverse('log-in')
        self.user = User.objects.get(username='johndoe')
        self.form_input = {
            'username':'johndoe', 'password':'Password123'
        }
        
    def test_successful_log_in(self):
        response = self.client.post(self.url, self.form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        response_url = reverse('dashboard')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        
    def test_unsuccessful_log_in(self):
        self.form_input['username'] = 'john'
        response = self.client.post(self.url, self.form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        response_url = reverse('log-in')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        
    def test_login_prohibited_mixin(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        response_url = reverse('dashboard')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)