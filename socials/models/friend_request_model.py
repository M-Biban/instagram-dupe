from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from .user_model import User
from .friendship_model import Friendship
from .follower_model import Follower
from django.core.exceptions import ValidationError

class FollowRequest(models.Model):
    from_user = models.ForeignKey(User, related_name = "from_user", on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name="to_user", on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if Follower.objects.filter(follower=self.from_user, user=self.to_user).exists():
            raise ValidationError("This follower relationship already exists.")
        if FollowRequest.objects.filter(from_user = self.from_user, to_user = self.to_user).exists():
            raise ValidationError("Already requested")
        if self.from_user == self.to_user:
            raise ValidationError("You can't follow yourself!")
        super().save(*args, **kwargs)

    
    def accept_request(self):
        self.accepted = True
        Follower.objects.create(
            user = self.to_user,
            follower = self.from_user
        )
        self.delete()
        
    def decline_request(self):
        self.delete()
    