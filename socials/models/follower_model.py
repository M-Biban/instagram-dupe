from django.db import models
from .user_model import User
from django.core.exceptions import ValidationError

class Follower(models.Model):
    current_user = models.ForeignKey(User, related_name="current_user", on_delete=models.CASCADE)
    follower = models.ForeignKey(User, related_name="follower", on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('current_user', 'follower')
        
    def save(self, *args, **kwargs):
        if Follower.objects.filter(follower=self.follower, current_user=self.current_user).exists():
            raise ValidationError("This follower relationship already exists.")
        if self.current_user == self.follower:
            raise ValidationError("You can't follow yourself!")
        super().save(*args, **kwargs)
        