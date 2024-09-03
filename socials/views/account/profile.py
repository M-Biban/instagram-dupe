from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, UpdateView
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from socials.forms import ConfirmPasswordForm, UserForm
from socials.models import User, Follower

@login_required
def view_profile(request):
    return render(request, 'account/view-profile.html',{'user': request.user, 'followers': Follower.objects.filter(user = request.user), 'following':Follower.objects.filter(follower = request.user),
                                                        'following_user_list': Follower.objects.filter(follower=request.user).values_list('user', flat=True)})

class DeleteProfileView(LoginRequiredMixin, FormView):
    
    form_class = ConfirmPasswordForm
    template_name = 'account/delete-profile.html'
    
    def get_object(self, queryset=None):
        """Return current user to be deleted"""
        return self.request.user
    
    def get_form_kwargs(self, **kwargs):
        """Pass the current user to the password change form."""
        kwargs = super().get_form_kwargs(**kwargs)
        kwargs.update({'user': self.request.user})
        return kwargs
    
    def form_valid(self, form):
        """Check form valid to confirm user deletion"""
        self.object = self.get_object()
        self.object.delete()
        messages.add_message(self.request, messages.SUCCESS, "Account deleted!")
        return redirect('home')
    
class EditProfileView(LoginRequiredMixin, UpdateView):
    """Display user profile editing screen, and handle profile modifications."""

    model = User
    template_name = "account/edit-profile.html"
    form_class = UserForm

    def get_object(self):
        """Return the object (user) to be updated."""
        user = self.request.user
        return user

    def get_success_url(self):
        """Return redirect URL after successful update."""
        messages.add_message(self.request, messages.SUCCESS, "Profile updated!")
        return reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)