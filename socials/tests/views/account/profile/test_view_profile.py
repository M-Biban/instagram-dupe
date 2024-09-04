"""Unit tests for the View Profile View."""
from django.test import TestCase
from socials.models import User, Follower, FollowRequest
from django.urls import reverse
from socials.tests.helpers import reverse_with_next

class ViewProfileViewTestCase(TestCase):
    """Unit tests for View Profile View."""

    fixtures = [
        'socials/tests/fixtures/default_user.json',
        'socials/tests/fixtures/other_users.json',
        'socials/tests/fixtures/default_friendship.json'
    ]
    
    def setUp(self):
        self.url = reverse('view-profile')
        self.user = User.objects.get(username = 'johndoe')
        self.other = User.objects.get(pk=3)
        self.new_follow = Follower.objects.create(
            user = self.other,
            follower = self.user
        )
        
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
        
    def test_context(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertQuerySetEqual(response.context['followers'], Follower.objects.filter(user = self.user))
        self.assertQuerySetEqual(response.context['following'], Follower.objects.filter(follower = self.user))
        self.assertQuerySetEqual(response.context['following_user_list'], Follower.objects.filter(follower=self.user).values_list('user', flat=True))
        self.assertQuerySetEqual(response.context['follower_user_list'], Follower.objects.filter(user=self.user).values_list('follower', flat=True))
        self.assertQuerySetEqual(response.context['follow_requests_made'], FollowRequest.objects.filter(from_user=self.user).values_list('to_user', flat=True))
        