from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from .user_model import User
from .friendship_model import Friendship
from .follower_model import Follower

class FollowRequest(models.Model):
    from_user = models.ForeignKey(User, related_name = "from_user", on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name="to_user", on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    
    def accept_request(self):
        self.accepted = True
        Follower.objects.create(
            current_user = self.from_user,
            follower = self.to_user
        )
        self.delete()
        
    def decline_request(self):
        self.delete()
    