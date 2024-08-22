from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from .user_model import User

class FollowRequest(models.Model):
    from_user = models.ForeignKey(User, related_name = "from_user", on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name="to_user", on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)