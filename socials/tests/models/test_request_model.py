"""Unit tests for the request model"""
from django.test import TestCase
from socials.models import FollowRequest, User, Friendship

class FollowRequestModelTestCase(TestCase):
    
    fixtures = [
        'socials/tests/fixtures/default_user.json',
        'socials/tests/fixtures/other_users.json',
        'socials/tests/fixtures/default_request.json'
    ]
    
    def setUp(self):
        self.user = User.objects.get(username='johndoe')
        self.other = User.objects.get(username='peterpickles')
        self.request = FollowRequest.objects.get(from_user = self.other, to_user = self.user)
        
    def test_accept_request(self):
        before_count_friendship = Friendship.objects.count()
        before_count_requests = FollowRequest.objects.count()
        self.request.accept_request()
        after_count_friendship = Friendship.objects.count()
        after_count_requests = FollowRequest.objects.count()
        self.assertEquals(before_count_friendship + 1, after_count_friendship)
        self.assertEquals(before_count_requests -1, after_count_requests)
        
    def test_default_accepted_value_is_false(self):
        before_count = Friendship.objects.count()
        request = FollowRequest.objects.create(
            from_user = self.user,
            to_user = self.other
        )
        self.assertEquals(request.accepted, False)
        after_count = Friendship.objects.count()
        self.assertEquals(before_count,after_count)
        
    def test_from_user_delete_on_cascade(self):
        before_count = FollowRequest.objects.count()
        self.other.delete()
        after_count = FollowRequest.objects.count()
        self.assertEquals(before_count - 2, after_count)
        
    def test_to_user_delete_on_cascade(self):
        before_count = FollowRequest.objects.count()
        self.user.delete()
        after_count = FollowRequest.objects.count()
        self.assertEquals(before_count - 1, after_count)