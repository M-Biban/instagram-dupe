from django.utils import timezone
from django.db import models
from .user_model import User
from .conversation_model import Conversation
from django.core.exceptions import ValidationError
from django.db.models import Q

class Friendship(models.Model):
    user1 = models.ForeignKey(User, related_name="user1", on_delete=models.CASCADE, blank=False)
    user2 = models.ForeignKey(User, related_name="user2", on_delete=models.CASCADE, blank=False)
    
    class Meta:
        unique_together = ('user1', 'user2')
        
    def save(self, *args, **kwargs):
        if Friendship.objects.filter(user1=self.user1, user2=self.user2).exists():
            raise ValidationError("This friendship relationship already exists.")
        if Friendship.objects.filter(user1=self.user2, user2=self.user1).exists():
            raise ValidationError("This friendship relationship already exists.")
        if self.user1 == self.user2:
            raise ValidationError("You can't friend yourself!")
        super().save(*args, **kwargs)