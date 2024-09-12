from django.db import IntegrityError, models
from socials.models import Post, User
from django.core.exceptions import ValidationError

class Like(models.Model):
    
    post = models.ForeignKey(Post, related_name="liked_post", on_delete=models.CASCADE)
    liked_by = models.ManyToManyField(User, related_name="liked_by", blank=True)
    