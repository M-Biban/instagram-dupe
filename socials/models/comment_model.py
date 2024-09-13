from django.db import models
from socials.models import Post, User

class Comment(models.Model):
    
    post = models.ForeignKey(Post, related_name="commented_post", on_delete=models.CASCADE)
    commented_by = models.ForeignKey(User, related_name="commented_by", on_delete=models.CASCADE)
    comment = models.CharField(max_length=350, blank=False)
    comment_time = models.DateTimeField(auto_now_add=True)