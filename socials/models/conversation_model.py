from django.db import models
from socials.models import User, Friendship
from django.core.exceptions import ValidationError

class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name="conversations")
    created_at = models.DateTimeField(null = False, blank = False)
    
    def clean(self):
        
        if self.participants.count() != 2:
            raise ValidationError("There must be exactly two people in the conversation")
        
        participants = self.participants.all()
        if Friendship.objects.filter(user1=participants[0], user2=participants[1]) is None and Friendship.objects.filter(user2=participants[1], user1=participants[0]) is None:
            raise ValidationError("You must be friends first!")
        
        if participants[0] == participants[1]:
            raise ValidationError("Can't have a conversation with yourself.")
        
        
    def save(self, *args, **kwargs):
        
        self.clean()
        super().save(*args, **kwargs)
        
        
    def __str__(self):
        return f"Conversation {self.id} - Participants: {', '.join([user.username for user in self.participants.all()])}"
    