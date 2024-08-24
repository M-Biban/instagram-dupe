"""Unit tests for the follower model"""
from django.test import TestCase
from socials.models import FollowRequest, User, Friendship, Follower

class FriendshipModelTestCase(TestCase):
    
    fixtures = [
        'socials/tests/fixtures/default_user.json',
        'socials/tests/fixtures/other_users.json',
        'socials/tests/fixtures/default_follower.json'
    ]
    
    def setUp(self):
        self.current_user = User.objects.get(username='petrapickles')
        self.follower = User.objects.get(username = 'peterpickles')
        self.followers = Follower.objects.get(current_user = self.current_user,
                                             follower = self.follower)
        
    def test_on_delete_cascade_current_user(self):
        before_count = self.get_count()
        self.current_user.delete()
        after_count = self.get_count()
        self.assertEquals(before_count-1, after_count)
        
    def test_on_delete_cascade_follower(self):
        before_count = self.get_count()
        self.follower.delete()
        after_count = self.get_count()
        self.assertEquals(before_count - 1, after_count)
        
    def test_no_follower_relationship_repeat(self):
        before_count = self.get_count()
        try:
            Follower.objects.create(
                current_user = self.current_user,
                follower = self.follower
            )
        except:
            pass
        self.assertEquals(before_count, self.get_count())
        
    def test_reverse_follower_is_allowed(self):
        before_count = self.get_count()
        try:
            Follower.objects.create(
                current_user = self.follower,
                follower = self.current_user
            )
        except:
            pass
        self.assertEquals(before_count+1, self.get_count())
        self.assertTrue(Friendship.objects.filter(user1=self.current_user, user2=self.follower).exists())
        
    def test_cannot_follow_yourself(self):
        before_count = self.get_count()
        try:
            Follower.objects.create(
                current_user = self.current_user,
                follower = self.current_user
            )
        except:
            pass
        self.assertEquals(before_count, self.get_count())
        
    def get_count(self):
        return Follower.objects.count()