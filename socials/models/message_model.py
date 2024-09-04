from django.db import models
from socials.models import User, Friendship
from django.core.exceptions import PermissionDenied, ValidationError

class Message(models.Model):
    _from = models.ForeignKey(User, related_name = "_from", on_delete=models.CASCADE)
    _to = models.ForeignKey(User, related_name="_to", on_delete=models.CASCADE)
    content = models.TextField(blank=False, help_text="Message...")
    date_time = models.DateTimeField(auto_now_add=True, blank=True)
    
    def save(self, *args, **kwargs):
        if Friendship.objects.filter(user1=self._from, user2=self._to) is None and Friendship.objects.filter(user2=self._from, user1=self._to) is None:
            raise ValidationError("You must be friends first!")
        if self._from == self._to:
            raise ValidationError("Can't send a message to yourself")
        super().save(*args, **kwargs)
        
    def delete_message(self):
        self.delete()
        
    def formatted_date(self):
        return self.date_time.strftime('%B %d, %Y at %I:%M %p')