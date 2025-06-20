"""Unit tests for the request model"""
from django.test import TestCase
from socials.models import FollowRequest, User, Friendship, Follower
from django.core.exceptions import ValidationError

class FollowRequestModelTestCase(TestCase):
    
    fixtures = [
        'socials/tests/fixtures/default_user.json',
        'socials/tests/fixtures/other_users.json',
        'socials/tests/fixtures/default_follower.json'
    ]
    
    def setUp(self):
        self.user = User.objects.get(username='johndoe')
        self.other = User.objects.get(username='peterpickles')
        self.user.private = True
        self.other.private = True
        self.request = FollowRequest.objects.create(from_user = self.other, to_user = self.user)
        
    def test_accept_request(self):
        before_count_friendship = Friendship.objects.count()
        before_count_follower = Follower.objects.count()
        before_count_requests = FollowRequest.objects.count()
        self.request.accept_request()
        after_count_follower = Follower.objects.count()
        after_count_requests = FollowRequest.objects.count()
        after_count_friendship = Friendship.objects.count()
        self.assertEqual(before_count_follower + 1, after_count_follower)
        self.assertEqual(before_count_requests -1, after_count_requests)
        self.assertEqual(before_count_friendship, after_count_friendship)
        
    def test_default_accepted_value_is_false(self):
        before_count = Follower.objects.count()
        self.other.private = True
        request = FollowRequest.objects.create(
            from_user = self.user,
            to_user = self.other
        )
        self.assertEqual(request.accepted, False)
        after_count = Follower.objects.count()
        self.assertEqual(before_count,after_count)
        
    def test_from_user_delete_on_cascade(self):
        before_count = FollowRequest.objects.count()
        self.other.delete()
        after_count = FollowRequest.objects.count()
        self.assertEqual(before_count - 1, after_count)
        
    def test_to_user_delete_on_cascade(self):
        before_count = FollowRequest.objects.count()
        self.user.delete()
        after_count = FollowRequest.objects.count()
        self.assertEqual(before_count - 1, after_count)
        
    def test_decline_request(self):
        before_count = FollowRequest.objects.count()
        self.request.decline_request()
        after_count = FollowRequest.objects.count()
        self.assertEqual(before_count - 1, after_count)
        
    def test_signal(self):
        self.user1 = User.objects.get(username = "janedoe")
        self.user2 = User.objects.get(username="petrapickles")
        before_count = Friendship.objects.count()
        Follower.objects.create(user=self.user1, follower=self.user2)
        
        # Ensure that no friendship exists yet
        self.assertFalse(Friendship.objects.filter(user1=self.user1, user2=self.user2).exists())
        
        # User2 follows User1
        Follower.objects.create(user=self.user2, follower=self.user1)
        
        # Now they should be friends
        self.assertTrue(Friendship.objects.filter(user1=self.user1, user2=self.user2).exists())
        
        # Check if the friendship is correctly created with the smaller user id as user1
        friendship = Friendship.objects.get(user1=self.user1, user2=self.user2)
        self.assertEqual(friendship.user1, self.user1)
        self.assertEqual(friendship.user2, self.user2)
        
        after_count  = Friendship.objects.count()
        self.assertEqual(before_count + 1, after_count)
        
    def test_cannot_request_exisiting_follower(self):
        self.user = User.objects.get(username = 'petrapickles')
        self.follower = User.objects.get(username='peterpickles')
        before_count = FollowRequest.objects.count()
        try:
            FollowRequest.objects.create(
                from_user = self.follower,
                to_user = self.user
            )
        except:
            pass
        
        after_count = FollowRequest.objects.count()
        self.assertEqual(before_count,after_count)
    
    def test_cannot_follow_yourself(self):
        self.request.from_user = self.user
        self.request.to_user = self.user
        self._assert_request_is_invalid()    
    
    def test_cannot_request_again(self):
        before_count = FollowRequest.objects.count()
        try:
            FollowRequest.objects.create(
                from_user = self.other,
                to_user = self.user
            )
        except:
            pass
        
        after_count = FollowRequest.objects.count()
        self.assertEqual(before_count,after_count)
    
    def _assert_request_is_valid(self):
        try:
            self.request.save()
        except (ValidationError):
            self.fail('Test user should be valid')

    def _assert_request_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.request.save()