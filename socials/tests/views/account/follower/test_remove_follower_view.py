"""Unit tests for the RemoveFollowerView."""
from django.test import TestCase
from socials.models import User, Follower
from django.urls import reverse
from django.contrib.messages import get_messages

class RemoveFollowerViewTestCase(TestCase):
    
    fixtures = [
        'socials/tests/fixtures/default_user.json',
        'socials/tests/fixtures/other_users.json',
        'socials/tests/fixtures/default_follower.json',
    ]
    
    def setUp(self):
        self.user = User.objects.get(pk = 3)
        self.follower = User.objects.get(pk = 4)
        self.follower_object = Follower.objects.get(pk=1)
        self.url = reverse('remove-follower', kwargs={'pk': self.follower_object.pk})
        
    def test_url(self):
        url = '/remove-follower/1/'
        self.assertEqual(self.url, url)
        
    def test_form_removes_follower(self):
        self.client.login(username=self.follower.username, password='Password123')
        response = self.client.post(self.url)
        self.assertFalse(Follower.objects.filter(pk=1).exists())
        self.assertRedirects(response, reverse('view-profile'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Follower removed successfully!")
        
    def test_only_follower_may_remove_follower(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.post(self.url)
        self.assertTrue(Follower.objects.filter(pk=1).exists())
        self.assertEqual(response.status_code, 403)
        
    def test_user_must_be_logged_in_else_redirected(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 403)
        # self.assertTemplateUsed(response, 'errors/403.html')
        