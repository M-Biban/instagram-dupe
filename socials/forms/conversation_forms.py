from socials.models import Message, GroupConversation, User, GCMessage
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
    
class GroupChatForm(forms.ModelForm):
    
    class Meta:
        model = GroupConversation
        fields = ['gc_name', 'participants']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['participants'].queryset = User.objects.all()
        
    def clean(self):
        cleaned_data = super().clean()
        participants = self.cleaned_data.get('participants')
        if participants.count() < 2:
            raise ValidationError("There must be at least 3 people in a gc")
        
        return cleaned_data
        
    def save(self, user, commit=True):
        """Create new gc"""
        gc = GroupConversation.objects.create(
            gc_name = self.cleaned_data.get('gc_name'),
            created_at = timezone.now()
        )
        gc.participants.set(self.cleaned_data.get('participants'))
        gc.participants.add(user)
        return gc
        
        
class GroupMessageForm(forms.ModelForm):

    class Meta:
        model = GCMessage
        fields = ['content']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.group_chat = kwargs.pop('group_chat', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        """Validate that the users are friends"""
        cleaned_data = super().clean()
        
        if self.group_chat is None:
            raise ValidationError("This group chat does not exist")
        
        if not self.group_chat.participants.filter(id=self.user.id).exists():
            raise ValidationError("You must be part of this conversation")
    
        return cleaned_data

    def save(self, commit=True):
        """Create a new message"""
        gcmessage = GCMessage.objects.create(
            group_chat = self.group_chat,
            gc_message_from=self.user,
            content=self.cleaned_data.get('content'),
            date_time=timezone.now()
        )
        gcmessage.seen_by.add(self.user)
        return gcmessage