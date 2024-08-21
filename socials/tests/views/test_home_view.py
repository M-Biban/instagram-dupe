"""Unit tests for the home View."""
from django.test import TestCase
from socials.models import User
from django.urls import reverse
from socials.tests.helpers import reverse_with_next

class DashboardViewTestCase(TestCase):
    """Unit tests for Sign Up View."""

    fixtures = [
        'socials/tests/fixtures/default_user.json'
    ]
    
    def setUp(self):
        self.url = reverse('home')
        self.user = User.objects.get(username='johndoe')
        
    def test_url(self):
        self.assertEqual(self.url, '/')
        
    def test_home_template(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        
    def test_login_prohibitied_mixin(self):
        self.client.login(username = self.user.username, password = 'Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        redirect_url = reverse('dashboard')
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)