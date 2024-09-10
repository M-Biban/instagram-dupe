from django.db import models
from .user_model import User
from django.core.exceptions import ValidationError
from django.db.models import Q

class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name="conversations", blank=True)
    created_at = models.DateTimeField(null = False, blank = False)
        
        
    def save(self, *args, **kwargs):
        
        super().save(*args, **kwargs)
        
    @classmethod
    def get_for_users(cls, user1, user2):
        return Conversation.objects.filter(participants=user1).filter(participants=user2).distinct()
        
        
    