from django.test import TestCase
from socials.models import FollowRequest, User, Friendship, Follower

class PrivateAccountTestCase(TestCase):
    
    fixtures = [
        'socials/tests/fixtures/default_user.json',
        'socials/tests/fixtures/other_users.json'
    ]
    
    def setUp(self):
        self.user = User.objects.get(username='johndoe')
        self.other = User.objects.get(username="janedoe")
        
    def test_default_is_set_to_false(self):
        new_user = User.objects.create(
            username = "valid",
            first_name = "valid",
            last_name = "valid",
            email = "valid@valid.com",
            password = "Password123"
        )
        self.assertFalse(new_user.private)
        
    def test_non_private_user_follows_automatically(self):
        before_count = Follower.objects.count()
        self.assertFalse(self.other.private)  #this is a public account
        before_count_request = FollowRequest.objects.count()
        FollowRequest.objects.create(
            from_user = self.user,
            to_user = self.other
        )
        after_count = Follower.objects.count()
        after_count_request = FollowRequest.objects.count()
        self.assertEqual(before_count + 1, after_count)
        self.assertEqual(before_count_request, after_count_request)
        
    def test_it_doesnt_work_vide_versa_of_one_above(self):
        before_count = Follower.objects.count()
        self.assertTrue(self.user.private)  #this is a private account
        self.assertFalse(self.other.private)  #this is a public account
        before_count_request = FollowRequest.objects.count()
        FollowRequest.objects.create(
            from_user = self.other,
            to_user = self.user
        )
        after_count = Follower.objects.count()
        after_count_request = FollowRequest.objects.count()
        self.assertEqual(before_count, after_count)
        self.assertEqual(before_count_request+1, after_count_request)