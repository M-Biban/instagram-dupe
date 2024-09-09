from socials.models import Message, Friendship, User
from django import forms
from django.utils import timezone
from django.core.exceptions import ValidationError

class MessageForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = ['content']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.to = kwargs.pop('to', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        """Validate that the users are friends"""
        cleaned_data = super().clean()
        _to_user = self.to
        _from_user = self.user
        friends = Friendship.objects.filter(user1=_to_user, user2=_from_user)
        friends2 = Friendship.objects.filter(user1=_from_user, user2=_to_user)
        if not friends.exists() and not friends2.exists():
            raise ValidationError("You are not friends yet!")
        return cleaned_data

    def save(self, _from, _to):
        """Create a new message"""
        message = Message.objects.create(
            _to=_to,
            _from=_from,
            content=self.cleaned_data.get('content'),
            date_time=timezone.now()
        )
        return message
