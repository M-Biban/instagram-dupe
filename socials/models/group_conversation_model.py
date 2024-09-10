from django.db import models
from .user_model import User

class GroupConversation(models.Model):
    
    gc_name = models.CharField(max_length= 100, unique=True, blank=False)
    participants = models.ManyToManyField(User, related_name="gc_participants", blank=True)
    created_at = models.DateTimeField(null = False, blank = False)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)