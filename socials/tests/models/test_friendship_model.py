"""Unit tests for the friendship model"""
from django.test import TestCase
from socials.models import FollowRequest, User, Friendship, Follower

class FriendshipModelTestCase(TestCase):
    
    fixtures = [
        'socials/tests/fixtures/default_user.json',
        'socials/tests/fixtures/other_users.json',
        'socials/tests/fixtures/default_friendship.json'
        ]
    
    def setUp(self):
        self.user = User.objects.get(username = 'johndoe')
        self.other = User.objects.get(username = 'petrapickles')
        self.friend = User.objects.get(username = 'janedoe')
        self.friendship = Friendship.objects.get(user1 = self.user, user2= self.friend)
        
    def test_friendship_creation(self):
        before_count = Friendship.objects.count()
        friendship = Friendship.objects.create(
            user1 = self.user,
            user2 = self.other
        )
        after_count = Friendship.objects.count()
        self.assertEqual(before_count+1, after_count)
        
    def test_no_repeat_friendship(self):
        before_count = Friendship.objects.count()
        try:
            friendship = Friendship.objects.create(
                user1 = self.friend,
                user2 = self.user
            )
        except:
            pass
        after_count = Friendship.objects.count()
        self.assertEqual(before_count, after_count)
        
    def test_cant_be_friends_with_yourself(self):
        before_count = Friendship.objects.count()
        try:
            friendship = Friendship.objects.create(
                user1 = self.user,
                user2 = self.user
            )
        except:
            pass
        after_count = Friendship.objects.count()
        self.assertEqual(before_count, after_count)
        
    
    