"""Unit tests for the Message Form."""
from django.test import TestCase
from socials.models import User, Conversation, Message
from socials.forms import MessageForm

class MessageFormTestCase(TestCase):
    """Unit tests for the Message Form."""
    
    fixtures = [
        'socials/tests/fixtures/default_user.json',
        'socials/tests/fixtures/other_users.json',
        'socials/tests/fixtures/default_conversation.json'
    ]
    
    def setUp(self):
        self.user = User.objects.get(username="johndoe")
        self.other = User.objects.get(username="janedoe")
        self.bad_user = User.objects.get(username="petrapickles")
        self.convo = Conversation.objects.get(pk=1)
        self.form_input = {'content': 'Test message'}
    
    def test_check_initialisation(self):
        form = MessageForm(user=self.user, conversation=self.convo, data = self.form_input)
        self.assertEqual(form.user, self.user)
        self.assertEqual(form.conversation, self.convo)
        
    def test_fields(self):
        form = MessageForm()
        self.assertIn('content', form.fields)
        
    def test_valid_form(self):
        form = MessageForm(user=self.user, conversation=self.convo, data = self.form_input)
        self.assertTrue(form.is_valid())
        
    def test_invalid_form(self):
        form = MessageForm(user=self.user, conversation=None, data = self.form_input)
        self.assertFalse(form.is_valid())
        
    def test_creates_new_message(self):
        before_count = Message.objects.count()
        form = MessageForm(user=self.user, conversation=self.convo, data = self.form_input)
        self.assertTrue(form.is_valid())
        message = form.save()
        self.assertEqual(message.conversation, self.convo)
        self.assertEqual(message.message_from, self.user)
        self.assertEqual(message.content, "Test message")
        after_count = Message.objects.count()
        self.assertEqual(after_count, before_count + 1)
    
    def test_clean_user_not_in_conversation(self):
        form = MessageForm(user=self.bad_user, conversation=self.convo, data = self.form_input)
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)
        self.assertIn("You must be part of this conversation", form.errors['__all__'])
        
    def test_clean_no_conversation(self):
        form = MessageForm(user=self.user, conversation=None, data = self.form_input)
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)
        self.assertIn("This conversation does not exist", form.errors['__all__'])
    
    def test_empty_message(self):
        input = {
            'content':''
        }
        form = MessageForm(user=self.user, conversation=self.convo, data = input)
        self.assertFalse(form.is_valid())

