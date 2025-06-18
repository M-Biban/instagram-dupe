"""Unit tests for the comment model"""
from django.test import TestCase
from socials.models import Conversation, User
from django.core.exceptions import ValidationError

class ConversationModelTestCase(TestCase):
    
    fixtures = [
        'socials/tests/fixtures/default_user',
        'socials/tests/fixtures/other_users',
        'socials/tests/fixtures/default_conversation'
    ]
    
    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.other_user = User.objects.get(pk=2)
        self.convo = Conversation.objects.get(pk=1)
        
    def test_conversation_is_retrieved(self):
        c = Conversation.get_for_users(self.user, self.other_user)
        self.assertEqual(len(c), 1)
        self.assertIn(self.user, c[0].participants.all())
        self.assertIn(self.other_user, c[0].participants.all())
        self.assertEqual(c[0], self.convo)