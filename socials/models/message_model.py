from django.db import models
from .user_model import User
from .conversation_model import Conversation
from django.core.exceptions import PermissionDenied, ValidationError

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, related_name="messages", on_delete=models.CASCADE, default=1)
    message_from = models.ForeignKey(User, related_name = "message_from", on_delete=models.CASCADE)
    content = models.TextField(blank=False, help_text="Message...")
    date_time = models.DateTimeField(null = False, blank = False)
    unread = models.BooleanField(default=True)
    
    def save(self, *args, **kwargs):
    
        if not self.conversation.participants.filter(id=self.message_from.id).exists():
            raise ValidationError("Sender must be a participant in the conversation")
        
        super().save(*args, **kwargs)
        
    def delete_message(self):
        self.delete()
        
    def formatted_date(self):
        return self.date_time.strftime('%B %d, %Y at %I:%M %p')
    
    def message_seen(self):
        self.unread = False