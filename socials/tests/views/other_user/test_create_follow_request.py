"""Unit tests for the Create follow request View."""
from django.test import TestCase
from socials.models import User, Follower, FollowRequest
from django.urls import reverse

class CreateFollowRequestViewTestCase(TestCase):
    
    fixtures = [
        'socials/tests/fixtures/default_user.json',
        'socials/tests/fixtures/other_users.json',
        'socials/tests/fixtures/default_follower.json'
    ]
    
    def setUp(self):
        self.current_user = User.objects.get(username = 'johndoe')
        self.user = User.objects.get(pk=3)
        self.user.private = True
        self.user.save()
        self.follower = User.objects.get(pk=4)
        self.url = reverse('create-follow-request', kwargs={'pk':self.user.pk})

        
    def test_url(self):
        url = '/create-follow-request/3/'
        self.assertEqual(url, self.url)
        
    def test_create_follow_request(self):
        self.client.login(username=self.current_user.username, password='Password123')
        before_count = FollowRequest.objects.count()
        response = self.client.post(self.url)
        after_count = FollowRequest.objects.count()
        self.assertEqual(before_count+1,after_count)
        
    def test_automatically_accept_request(self):
        self.user.private = False
        self.user.save()
        self.client.login(username=self.current_user.username, password='Password123')
        b_follower = Follower.objects.count()
        before_count = FollowRequest.objects.count()
        self.client.post(self.url)
        after_count = FollowRequest.objects.count()
        a_follower = Follower.objects.count()
        self.assertEqual(before_count,after_count)
        self.assertEqual(b_follower+1, a_follower)
        self.assertTrue(Follower.objects.filter(follower = self.current_user, user = self.user).exists())
        
    def test_no_duplication_allowed(self):
        self.client.login(username = self.follower.username, password='Password123')
        url = reverse('create-follow-request', kwargs={'pk':self.user.pk})
        b_follower = Follower.objects.count()
        before_count = FollowRequest.objects.count()
        self.client.post(url)
        after_count = FollowRequest.objects.count()
        a_follower = Follower.objects.count()
        self.assertEqual(before_count,after_count)
        self.assertEqual(b_follower, a_follower)