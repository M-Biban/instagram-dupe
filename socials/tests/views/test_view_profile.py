"""Unit tests for the View Profile View."""
from django.test import TestCase
from socials.models import User
from django.urls import reverse
from socials.tests.helpers import reverse_with_next

class ViewProfileViewTestCase(TestCase):
    """Unit tests for Sign Up View."""

    fixtures = [
        'socials/tests/fixtures/default_user.json'
    ]
    
    def setUp(self):
        self.url = reverse('view-profile')
        self.user = User.objects.get(username = 'johndoe')
        
    def test_view_profile_url(self):
        self.assertEqual(self.url, '/view-profile/')
        
    def test_login_required_helper(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_with_next('log-in', self.url))
        
    def test_logged_in_user(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'account/view-profile.html')
        user = response.context['user']
        self.assertEquals(self.user, user)
        