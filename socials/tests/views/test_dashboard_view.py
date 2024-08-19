"""Unit tests for the dashboard View."""
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
        self.url = reverse('dashboard')
        self.user = User.objects.get(username='johndoe')
        
    def test_dashboard_url(self):
        required_url = '/dashboard/'
        self.assertEquals(self.url, required_url)
        
    def test_dashboard_context(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'dashboard.html')
        user = response.context['user']
        self.assertEquals(self.user, user)
    
    def test_login_required(self):
        redirect_url = reverse_with_next('log-in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        