from django.db import models
from .user_model import User
from .group_conversation_model import GroupConversation
from django.core.exceptions import PermissionDenied, ValidationError

class GCMessage(models.Model):
    group_chat = models.ForeignKey(GroupConversation, related_name="group_chat", on_delete=models.CASCADE, default=1)
    gc_message_from = models.ForeignKey(User, related_name = "gc_message_from", on_delete=models.CASCADE)
    content = models.TextField(blank=False, help_text="Message...")
    date_time = models.DateTimeField(null = False, blank = False)
    seen_by = models.ManyToManyField(User, related_name='seen_group_messages', blank=True)
    
    def save(self, *args, **kwargs):
        
        super().save(*args, **kwargs)
        
    def delete_message(self):
        self.delete()
        
    def formatted_date(self):
        return self.date_time.strftime('%B %d, %Y at %I:%M %p')
    
    def message_seen(self):
        self.unread = False
        
    def mark_as_seen(self, user):
        if user in self.conversation.participants.all():
            self.seen_by.add(user)
            self.save()
            
    def is_seen_by(self, user):
        return self.seen_by.filter(id=user.id).exists()