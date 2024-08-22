from django.db import models
from .user_model import User

class Follower(models.Model):
    current_user = models.ForeignKey(User, related_name="current_user", on_delete=models.CASCADE)
    follower = models.ForeignKey(User, related_name="follower", on_delete=models.CASCADE)