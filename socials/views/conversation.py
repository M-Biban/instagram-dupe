from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from socials.forms import MessageForm
from django.contrib import messages
from django.urls import reverse

class CreateMessageView(LoginRequiredMixin, FormView):
    """Create new message"""
    
    form_class = MessageForm
    template_name = "conversation/create_message.html"
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Pass the current user to the form
        return kwargs
    
    def form_valid(self, form):
        user = self.request.user
        form.save(_from=user)
        messages.success(self.request, "Message sent!")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context
    
    def get_success_url(self):
        return reverse("dashboard")
    