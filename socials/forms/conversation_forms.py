from socials.models import Message, Friendship, User
from django import forms
from django.utils import timezone
from django.core.exceptions import ValidationError

class MessageForm(forms.ModelForm):
    
    class Meta:
        
        model = Message
        fields = ['content', '_to']
        
    def clean(self):
        """Validate users"""
        cleaned_data = super().clean()
        _to_user = cleaned_data.get('_to')
        _from_user = self.user
        friends = Friendship.objects.filter(user1 = _to_user, user2 = _from_user)
        friends2 = Friendship.objects.filter(user1 = _from_user, user2 = _to_user)
        if not friends.exists() and not friends2.exists():
            return ValidationError("You are not friends yet!")
        
        return cleaned_data
    
    def __init__(self, *args, **kwargs):
        # Get the current user from the view
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Filter the '_to' field queryset
        if self.user:
            friends1 = Friendship.objects.filter(user1 = self.user).values_list('user2', flat=True)
            friends2 = Friendship.objects.filter(user2 = self.user).values_list('user1', flat=True)
            ids = []
            for t in friends1:
                ids.append(t)
            for t in friends2:
                ids.append(t)
            self.fields['_to'].queryset = User.objects.filter(id__in=ids) 
        
    def save(self, _from):
        """Create new Message"""
        
        super().save(commit=False)
        message = Message.objects.create(
            _to = self.cleaned_data.get('_to'),
            _from = _from,
            content = self.cleaned_data.get('content'),
            date_time = timezone.now()
        )
        
        return message