from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.contrib import messages
from django.urls import reverse
from socials.models import User, Friendship
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from socials.forms import MessageForm

class CreateMessageView(LoginRequiredMixin, FormView):
    """Create new message"""

    form_class = MessageForm
    template_name = "conversation/create_message.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Pass the current user to the form
        kwargs['to'] = self.get_object()  # Pass the recipient user to the form
        return kwargs

    def get_object(self, queryset=None):
        """Get the recipient user"""
        user_pk = self.kwargs.get('pk')
        user = get_object_or_404(User, pk=user_pk)
        return user

    def dispatch(self, request, *args, **kwargs):
        recipient = self.get_object()
        if not Friendship.objects.filter(user1=request.user, user2=recipient).exists() and not Friendship.objects.filter(user2=request.user, user1=recipient).exists():
            raise PermissionDenied("You must be friends to message each other!")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = self.request.user
        recipient = self.get_object()
        form.save(_from=user, _to=recipient)
        messages.success(self.request, "Message sent!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        context['to'] = self.get_object()
        context['open_messages_sidebar'] = True
        return context

    def get_success_url(self):
        return reverse("dashboard")
