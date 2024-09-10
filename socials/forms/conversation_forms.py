from socials.models import Message, Friendship, User, Conversation
from django import forms
from django.utils import timezone
from django.core.exceptions import ValidationError

class MessageForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = ['content']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.conversation = kwargs.pop('conversation', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        """Validate that the users are friends"""
        cleaned_data = super().clean()
        
        if self.conversation is None:
            raise ValidationError("This conversation does not exist")
        
        if not self.conversation.participants.filter(id=self.user.id).exists():
            raise ValidationError("You must be part of this conversation")
    
        return cleaned_data

    def save(self, commit=True):
        """Create a new message"""
        message = Message.objects.create(
            conversation = self.conversation,
            message_from=self.user,
            content=self.cleaned_data.get('content'),
            date_time=timezone.now()
        )
        return message
