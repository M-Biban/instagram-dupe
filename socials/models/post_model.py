from django.db import models
from .user_model import User

class Post(models.Model):
    caption = models.CharField(max_length=300, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)