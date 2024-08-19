"""Unit tests for the log out request."""
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
        self.url = reverse('log-out')
        self.user = User.objects.get(username='johndoe')
        
    def test_log_out_url(self):
        self.assertEquals(self.url, '/log-out/')
        
    def test_log_out_works(self):
        """Test that accessing the log_out view logs out the user."""
        # Ensure the user is logged in before the logout
        expected_url = reverse_with_next('log-in', self.url)
        response = self.client.get(reverse('log-out'))
        self.assertRedirects(response, expected_url)
        
        # After logout, the user should no longer be authenticated
        response = self.client.get(reverse('home'))
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        
    def test_must_be_logged_in(self):
        
        self.client.login(username =self. user.username, password='Password123')
        response = self.client.get(reverse('log-out'))
        self.assertEqual(response.status_code, 302)
        