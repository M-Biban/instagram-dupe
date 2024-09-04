from django.db import models
from socials.models import User, Friendship
from django.core.exceptions import ValidationError

class Follower(models.Model):
    user = models.ForeignKey(User, related_name="user", on_delete=models.CASCADE)
    follower = models.ForeignKey(User, related_name="follower", on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('user', 'follower')
        
    def save(self, *args, **kwargs):
        if Follower.objects.filter(follower=self.follower, user=self.user).exists():
            raise ValidationError("This follower relationship already exists.")
        if self.user == self.follower:
            raise ValidationError("You can't follow yourself!")
        super().save(*args, **kwargs)
        
    def remove_follower(self):
        self.delete()
        
    def unfollow(self):
        if Friendship.objects.filter(user1 = self.user, user2= self.follower).exists():
            Friendship.objects.get(user1=self.user, user2=self.follower).delete()
        elif Friendship.objects.filter(user2 = self.user, user1= self.follower).exists():
            Friendship.objects.get(user2=self.user, user1=self.follower).delete()
        self.delete()
        