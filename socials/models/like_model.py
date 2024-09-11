from django.db import models
from socials.models import Post, User

class Like(models.Model):
    
    post = models.ForeignKey(Post, related_name="liked_post", on_delete=models.CASCADE)
    liked_by = models.ManyToManyField(User, related_name="liked_by", blank=True)
    
    def get_likes(self):
        return self.count