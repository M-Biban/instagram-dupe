from django.db import models
from .user_model import User

class Friendship(models.Model):
    user1 = models.ForeignKey(User, related_name="user1", on_delete=models.CASCADE, blank=False)
    user2 = models.ForeignKey(User, related_name="user2", on_delete=models.CASCADE, blank=False)