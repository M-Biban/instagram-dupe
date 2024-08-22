from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from .user_model import User
from .friendship_model import Friendship

class FollowRequest(models.Model):
    from_user = models.ForeignKey(User, related_name = "from_user", on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name="to_user", on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    
    def accept_request(self):
        self.accepted = True
        Friendship.objects.create(
            user1 = self.from_user,
            user2 = self.to_user
        )
        self.delete()
    