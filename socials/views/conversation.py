from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView, CreateView
from django.contrib import messages
from django.urls import reverse
from socials.models import User, Conversation, Friendship, Message, GroupConversation, GCMessage
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from socials.forms import MessageForm, GroupChatForm, GroupMessageForm
from django.db.models import Q

class CreateMessageView(LoginRequiredMixin, FormView):
    """Create new message"""

    form_class = MessageForm
    template_name = "conversation/create_message.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Pass the current user to the form
        kwargs['conversation'] = self.get_conversation()
        return kwargs

    def get_object(self, queryset=None):
        """Get the recipient user"""
        user_pk = self.kwargs.get('pk')
        to_user = get_object_or_404(User, pk=user_pk)
        return to_user
    
    def get_conversation(self):
        user = self.get_object()
        conversation = Conversation.get_for_users(user1 = self.request.user, user2 = user)
        return conversation[0]

    def dispatch(self, request, *args, **kwargs):
        recipient = self.get_object()
        if not Friendship.objects.filter(user1=request.user, user2=recipient).exists() and not Friendship.objects.filter(user2=request.user, user1=recipient).exists():
            raise PermissionDenied("You must be friends to message each other!")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Message sent!")
        return super().form_valid(form)
    
    def get_messages(self):
        conversation = self.get_conversation()
        messages = Message.objects.filter(conversation = conversation)
        return messages
    
    def get_unread_messages(self):
        conversation = self.get_conversation()
        unread = Message.objects.filter(conversation= conversation, unread = True)
        return unread
    
    def see_messages(self):
        messages = self.get_unread_messages()
        for message in messages:
            if message.message_from != self.request.user:
                message.message_seen()
                message.save()
            
    
    def get(self, request, *args, **kwargs):
        """Handle GET request and mark messages as seen."""
        self.see_messages()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        context['to'] = self.get_object()
        context['open_messages_sidebar'] = True
        context['conversation'] = self.get_conversation()
        context['user_messages'] = self.get_messages()
        return context

    def get_success_url(self):
        return reverse("dashboard")
    
class CreateGroupChatView(LoginRequiredMixin, FormView):
    
    template_name = "conversation/create_gc.html"
    form_class = GroupChatForm
    
    def get_user(self):
        return self.request.user
    
    def form_valid(self, form):
        user = self.get_user()
        group_conversation = form.save(commit=False, user = user)
        # Ensure the creator is added as a participant
        group_conversation.participants.add(self.request.user)
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context
    
    def get_success_url(self):
        return reverse("dashboard")

class CreateGCMessageView(LoginRequiredMixin, FormView):
    """Create new message"""

    form_class = GroupMessageForm
    template_name = "conversation/create_gc_message.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['group_chat'] = self.get_object()
        return kwargs
    
    def dispatch(self, request, *args, **kwargs):
        gc = self.get_object()
        if not gc.participants.filter(id=request.user.id).exists():
            raise PermissionDenied("You are not part of this gc")
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        """Get the conversations"""
        convo_pk = self.kwargs.get('pk')
        convo = get_object_or_404(GroupConversation, pk=convo_pk)
        return convo

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Message sent!")
        return super().form_valid(form)
    
    def get_messages(self):
        groupchat = self.get_object()
        messages = GCMessage.objects.filter(group_chat = groupchat)
        return messages
    
    def get_unread_messages(self):
        groupchat = self.get_object()
        unread = GCMessage.objects.filter(group_chat= groupchat).exclude(seen_by=self.request.user)
        return unread
    
    def mark_messages_as_seen(self):
        unread = self.get_unread_messages()
        for message in unread:
            message.seen_by.add(self.request.user)
    
    def get(self, request, *args, **kwargs):
        """Handle GET request and mark messages as seen."""
        self.mark_messages_as_seen()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        context['open_messages_sidebar'] = True
        context['group_chat'] = self.get_object()
        return context

    def get_success_url(self):
        return reverse("dashboard")