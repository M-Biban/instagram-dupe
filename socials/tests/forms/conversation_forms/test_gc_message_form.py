"""Unit tests for the Group Chat Message Form."""
from django.test import TestCase
from socials.models import User, GroupConversation, GCMessage
from socials.forms import GroupMessageForm

class GCMessageFormTestCase(TestCase):
    """Unit tests for the Group Chat Form."""
    
    fixtures = [
        'socials/tests/fixtures/default_user.json',
        'socials/tests/fixtures/other_users.json',
        'socials/tests/fixtures/default_gc.json'
    ]
    
    def setUp(self):
        
        self.gc = GroupConversation.objects.get(pk=1)
        self.user = User.objects.get(username="johndoe")
        self.form_input = {
            "content" : "test gc message"
        }
        
    def test_form_has_correct_fields(self):
        
        form = GroupMessageForm()
        self.assertIn('content', form.fields)
        
    def test_valid_form(self):
        
        form = GroupMessageForm(group_chat= self.gc, user = self.user, data=self.form_input)
        self.assertTrue(form.is_valid())
        
    def test_new_gc_message_created(self):
        before_count = GCMessage.objects.count()
        form = GroupMessageForm(group_chat= self.gc, user = self.user, data=self.form_input)
        self.assertTrue(form.is_valid())
        message = form.save()
        self.assertEqual(message.group_chat, self.gc)
        self.assertEqual(message.gc_message_from, self.user)
        self.assertEqual(message.content, "test gc message")
        self.assertIn(self.user, message.seen_by.all())
        after_count = GCMessage.objects.count()
        self.assertEqual(before_count+1, after_count)
        
    def test_invalid_if_group_chat_does_not_exist(self):
        form = GroupMessageForm(group_chat= None, user = self.user, data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)
        self.assertIn("This group chat does not exist", form.errors['__all__'])
        
    def test_invalid_if_user_not_in_group_chat(self):
        rand_user = User.objects.get(pk=4)
        form = GroupMessageForm(group_chat= self.gc, user = rand_user, data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)
        self.assertIn("You must be part of this conversation", form.errors['__all__'])