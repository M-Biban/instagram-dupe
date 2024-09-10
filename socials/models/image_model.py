from django.db import models
from .user_model import User
from .post_model import Post

class Image(models.Model):
    post = models.ForeignKey(Post, related_name="images")
    image = models.ImageField(upload_to='post-images/')
    