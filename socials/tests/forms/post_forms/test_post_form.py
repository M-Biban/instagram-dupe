"""Unit tests for the Post Form."""
from django.test import TestCase
from socials.models import User
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
        
    