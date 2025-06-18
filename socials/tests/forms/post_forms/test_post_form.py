"""Unit tests for the Post Form."""
from django.test import TestCase
from socials.models import User, Post
from socials.forms import PostForm

class PostFormTestCase(TestCase):
    """Unit tests for the Post Form."""
    
    fixtures = [
        'socials/tests/fixtures/default_user'
    ]
    
    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.form_input = {
            "caption" : "Test caption"
        }
        
    def test_form_fields(self):
        form = PostForm()
        self.assertIn('caption', form.fields)
        self.assertNotIn('user', form.fields)
    
    def test_empty_caption_allowed(self):
        self.form_input["caption"] = ""
        form = PostForm(data = self.form_input)
        self.assertTrue(form.is_valid())
        
    def test_new_post_created(self):
        before_count = Post.objects.count()
        form = PostForm(data = self.form_input)
        self.assertTrue(form.is_valid())
        post = form.save(user = self.user)
        after_count = Post.objects.count()
        self.assertEqual(before_count + 1, after_count)
        self.assertEqual(post.caption, "Test caption")
        self.assertEqual(post.user, self.user)
        
    