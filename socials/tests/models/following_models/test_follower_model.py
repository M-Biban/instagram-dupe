"""Unit tests for the follower model"""
from django.test import TestCase
from socials.models import FollowRequest, User, Friendship, Follower

class FollowerModelTestCase(TestCase):
    
    fixtures = [
        'socials/tests/fixtures/default_user.json',
        'socials/tests/fixtures/other_users.json',
        'socials/tests/fixtures/default_follower.json',
        'socials/tests/fixtures/default_friendship.json'
    ]
    
    def setUp(self):
        self.user = User.objects.get(username='petrapickles')
        self.follower = User.objects.get(username = 'peterpickles')
        self.followers = Follower.objects.get(pk = 1)
        
    def test_on_delete_cascade_user(self):
        before_count = self.get_count()
        self.user.delete()
        after_count = self.get_count()
        self.assertEqual(before_count-1, after_count)
        
    def test_on_delete_cascade_follower(self):
        before_count = self.get_count()
        self.follower.delete()
        after_count = self.get_count()
        self.assertEqual(before_count - 1, after_count)
    
    def test_removing_follower_does_not_delete_user(self):
        before_count = User.objects.count()
        self.followers.remove_follower()
        after_count = User.objects.count()
        self.assertEqual(before_count, after_count)
        
    def test_remove_follower(self):
        before_count = Follower.objects.count()
        self.followers.remove_follower()
        after_count = Follower.objects.count()
        self.assertEqual(before_count - 1, after_count)
        
    def test_unfollow(self):
        before_count = Follower.objects.count()
        self.followers.unfollow()
        after_count = Follower.objects.count()
        self.assertEqual(before_count - 1, after_count)
        
    def test_unfollow_friendship(self):
        before_count = Follower.objects.count()
        Follower.objects.get(pk=2).unfollow()
        after_count = Follower.objects.count()
        self.assertEqual(before_count - 1, after_count)
        
    def test_unfollow_friendship1(self):
        before_count = Follower.objects.count()
        Follower.objects.get(pk=3).unfollow()
        after_count = Follower.objects.count()
        self.assertEqual(before_count - 1, after_count)
        
        
    def test_no_follower_relationship_repeat(self):
        before_count = self.get_count()
        try:
            Follower.objects.create(
                user = self.user,
                follower = self.follower
            )
        except:
            pass
        self.assertEqual(before_count, self.get_count())
        
    def test_reverse_follower_is_allowed(self):
        before_count = self.get_count()
        try:
            Follower.objects.create(
                user = self.follower,
                follower = self.user
            )
        except:
            pass
        self.assertEqual(before_count+1, self.get_count())
        self.assertTrue(Friendship.objects.filter(user1=self.user, user2=self.follower).exists())
        
    def test_cannot_follow_yourself(self):
        before_count = self.get_count()
        try:
            Follower.objects.create(
                user = self.user,
                follower = self.user
            )
        except:
            pass
        self.assertEqual(before_count, self.get_count())
        
    def get_count(self):
        return Follower.objects.count()