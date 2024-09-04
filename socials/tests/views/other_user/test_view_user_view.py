"""Unit tests for the View UserView."""
from django.test import TestCase
from socials.models import User, Follower
from django.urls import reverse

class ViewUserViewTestCase(TestCase):
    """Unit tests for View User View."""
    
    fixtures = [
        'socials/tests/fixtures/default_user.json',
        'socials/tests/fixtures/other_users.json',
        'socials/tests/fixtures/default_follower.json',
        'socials/tests/fixtures/default_private_follower.json'
    ]
    
    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.other = User.objects.get(pk=3)
        self.private_user = User.objects.get(pk=5)
        self.private_follower_object = Follower.objects.get(pk=2)
        self.url = reverse('view_user', kwargs={'pk': 3})
        
    def test_url(self):
        url = '/view_user/3/'
        self.assertEqual(self.url, url)
        
    def test_context(self):
        self.client.login(username = self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['profile_user'], self.other)
        self.assertEquals(response.context['user_followers'].count(), 1)
        self.assertEquals(response.context['user_is_following'].count(), 1)
        
    def test_user_views_their_own_profile(self):
        url = reverse('view_user', kwargs={'pk':1})
        self.client.login(username = self.user.username, password='Password123')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('view-profile'))
        
    def test_can_access_user_if_private_and_not_following(self):
        url = reverse('view_user', kwargs={'pk':5})
        self.client.login(username = self.user.username, password='Password123')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
    def test_can_access_private_user_if_following(self):
        url = reverse('view_user', kwargs={'pk':5})
        self.client.login(username = self.other.username, password='Password123')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)