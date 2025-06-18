"""Unit tests for the comment model"""
from django.test import TestCase
from socials.models import Post, User, Comment
from django.core.exceptions import ValidationError

class CommentModelTestCase(TestCase):
    
    fixtures = [
        'socials/tests/fixtures/default_post',
        'socials/tests/fixtures/default_user',
        'socials/tests/fixtures/other_users',
        'socials/tests/fixtures/default_comment',
    ]
    
    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.commenter = User.objects.get(pk=2)
        self.post = Post.objects.get(pk=1)
        self.comment_1 = Comment.objects.get(pk=1)
        self.comment_2 = Comment.objects.get(pk=2)
        
    def test_on_delete_cascade_post(self):
        before_count = Comment.objects.count()
        self.post.delete()
        after_count = Comment.objects.count()
        self.assertEqual(before_count - 2, after_count)
        
    def test_on_delete_cascade_commented_by(self):
        before_count = Comment.objects.count()
        self.commenter.delete()
        after_count = Comment.objects.count()
        self.assertEqual(before_count-1, after_count)
        
    def test_on_delete_cascade_user(self):
        before_count = Comment.objects.count()
        self.user.delete()
        after_count = Comment.objects.count()
        self.assertEqual(before_count - 2, after_count)
        
    def test_maximum_comment_length(self):
        self.comment_1.comment = "a" * 351
        self._assert_comment_is_invalid()
        
    def test_comment_cannot_be_blank(self):
        self.comment_1.comment = ""
        self._assert_comment_is_invalid()
        
    def _assert_comment_is_valid(self):
        try:
            self.comment_1.full_clean()
        except (ValidationError):
            self.fail('Test user should be valid')

    def _assert_comment_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.comment_1.full_clean()