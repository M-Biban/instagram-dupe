"""Unit tests for the Group Chat Form."""
from django.test import TestCase
from socials.models import User, GroupConversation
from socials.forms import GroupChatForm

class GCFormTestCase(TestCase):
    """Unit tests for the Group Chat Form."""
    
    fixtures = [
        'socials/tests/fixtures/default_user.json',
        'socials/tests/fixtures/other_users.json'
    ]
    
    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)
        self.user3 = User.objects.get(pk=3)
        self.user4 = User.objects.get(pk=4)
        self.participants = [self.user4, self.user2, self.user3]
        self.form_input = {
            'gc_name': "test gc",
            'participants': self.participants 
            }
        
    def test_form_fields(self):
        form = GroupChatForm()
        self.assertIn('gc_name', form.fields)
        self.assertIn('participants', form.fields)
        
    def test_valid_form(self):
        form = GroupChatForm(data = self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_new_gc_made(self):
        before_count = GroupConversation.objects.count()
        form = GroupChatForm(data = self.form_input)
        self.assertTrue(form.is_valid())
        gc = form.save(self.user)
        self.assertEqual(gc.gc_name, 'test gc')
        after_count = GroupConversation.objects.count()
        self.assertEqual(before_count + 1, after_count)
        self.assertIn(self.user, gc.participants.all())
        self.assertIn(self.user2, gc.participants.all())
        self.assertIn(self.user3, gc.participants.all())
        self.assertIn(self.user4, gc.participants.all())
        
    def test_min_number_of_participants(self):
        before_count = GroupConversation.objects.count()
        self.form_input['participants'] = [self.user2]
        form = GroupChatForm(data = self.form_input)
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)
        self.assertIn("There must be at least 3 people in a gc", form.errors['__all__'])
        after_count = GroupConversation.objects.count()
        self.assertEqual(before_count, after_count)