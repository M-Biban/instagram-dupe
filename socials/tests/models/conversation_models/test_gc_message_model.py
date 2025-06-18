"""Unit tests for the gc message model"""
from django.test import TestCase
from socials.models import GroupConversation, GCMessage, User
from django.core.exceptions import ValidationError

class GCMessageModelTestCase(TestCase):
    
    fixtures = [
        'socials/tests/fixtures/default_gc.json',
        'socials/tests/fixtures/default_user.json',
        'socials/tests/fixtures/other_users.json',
        'socials/tests/fixtures/default_gc_message.json'
    ]
    
    def setUp(self):
        self.gc = GroupConversation.objects.get(pk=1)
        self.gc_message = GCMessage.objects.get(pk=1)
        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)
        self.user3 = User.objects.get(pk=3)
        self.user4 = User.objects.get(pk=4)
        
    def test_on_delete_cascade_gc(self):
        before_count = GCMessage.objects.count()
        self.gc.delete()
        after_count = GCMessage.objects.count()
        self.assertEqual(before_count-1, after_count)
    
    def test_on_delete_cascade_message_from(self):
        before_count = GCMessage.objects.count()
        self.user1.delete()
        after_count = GCMessage.objects.count()
        self.assertEqual(before_count-1, after_count)
        
    def test_content_cannot_be_blank(self):
        self.gc_message.content = ""
        self._assert_message_is_invalid()
        
    def test_date_time_cannot_be_null(self):
        self.gc_message.date_time = None
        self._assert_message_is_invalid() 
    
    def test_delete_message_method(self):
        before_count = GCMessage.objects.count()
        self.gc_message.delete_message()
        after_count = GCMessage.objects.count()
        self.assertEqual(before_count-1, after_count)
        self.assertFalse(GCMessage.objects.filter(pk=1).exists())
        
    def test_formatted_date_method(self):
        formatted = self.gc_message.formatted_date()
        self.assertEqual(formatted, "June 17, 2025 at 12:38 PM")
        
    def test_mark_as_seen_in_gc(self):
        before_count = self.gc_message.seen_by.count()
        self.gc_message.mark_as_seen(self.user3)
        after_count = self.gc_message.seen_by.count()
        self.assertEqual(before_count+1, after_count)
        
    def test_mark_as_seen_not_in_gc(self):
        before_count = self.gc_message.seen_by.count()
        self.gc_message.mark_as_seen(self.user4)
        after_count = self.gc_message.seen_by.count()
        self.assertEqual(before_count, after_count)
        
    def test_mark_as_seen_no_duplicates(self):
        before_count = self.gc_message.seen_by.count()
        self.gc_message.mark_as_seen(self.user2)
        after_count = self.gc_message.seen_by.count()
        self.assertEqual(before_count, after_count)
        
    def test_is_seen_by_returns_true(self):
        self.assertTrue(self.gc_message.is_seen_by(self.user2))
        
    def test_is_seen_by_returns_false(self):
        self.assertFalse(self.gc_message.is_seen_by(self.user3))
        
        
    def _assert_message_is_valid(self):
        try:
            self.gc_message.full_clean()
        except (ValidationError):
            self.fail('Test user should be valid')

    def _assert_message_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.gc_message.full_clean()