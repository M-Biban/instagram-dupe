# socials/views.py
from django.shortcuts import render, redirect
from django.views.generic import FormView, View, UpdateView
from django.contrib.auth import login, logout
from .forms import SignUpForm, LogInForm, ConfirmPasswordForm, UserForm
from .models import User, Follower
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from socials.helpers import login_prohibited
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.mixins import LoginRequiredMixin

@login_prohibited
def home(request):
    return render(request, 'index.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html',{'user': request.user})

class LoginProhibitedMixin:
    """Mixin that redirects when a user is logged in."""

    redirect_when_logged_in_url = None

    def dispatch(self, *args, **kwargs):
        """Redirect when logged in, or dispatch as normal otherwise."""
        if self.request.user.is_authenticated:
            return self.handle_already_logged_in(*args, **kwargs)
        return super().dispatch(*args, **kwargs)

    def handle_already_logged_in(self, *args, **kwargs):
        url = self.get_redirect_when_logged_in_url()
        return redirect(url)

    def get_redirect_when_logged_in_url(self):
        """Returns the url to redirect to when not logged in."""
        if self.redirect_when_logged_in_url is None:
            raise ImproperlyConfigured(
                "LoginProhibitedMixin requires either a value for "
                "'redirect_when_logged_in_url', or an implementation for "
                "'get_redirect_when_logged_in_url()'."
            )
        else:
            return self.redirect_when_logged_in_url

class SignUpView(LoginProhibitedMixin, FormView):
    form_class = SignUpForm
    template_name = "sign-up.html"
    redirect_when_logged_in_url = settings.REDIRECT_URL_WHEN_LOGGED_IN

    def form_valid(self, form):
        self.object = form.save()
        login(self.request, self.object)
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, "Please correct the errors below and try again!")
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, "Account created!")
        return reverse(self.redirect_when_logged_in_url)


class LogInView(LoginProhibitedMixin, FormView):
    form_class = LogInForm
    template_name = "log-in.html"
    redirect_when_logged_in_url = settings.REDIRECT_URL_WHEN_LOGGED_IN


    def form_valid(self, form):
        login(self.request, form.get_user())
        return redirect(self.get_success_url())
    
    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, "The credentials provided were invalid!")
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse(self.redirect_when_logged_in_url)
    

@login_required
def log_out(request):
    """Log out the current user"""

    logout(request)
    return redirect('home')

@login_required
def view_profile(request):
    return render(request, 'view-profile.html',{'user': request.user, 'followers': Follower.objects.filter(current_user = request.user)})

class DeleteAccountView(LoginRequiredMixin, FormView):
    
    form_class = ConfirmPasswordForm
    template_name = 'delete-profile.html'
    
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
    
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Display user profile editing screen, and handle profile modifications."""

    model = User
    template_name = "edit-profile.html"
    form_class = UserForm

    def get_object(self):
        """Return the object (user) to be updated."""
        user = self.request.user
        return user

    def get_success_url(self):
        """Return redirect URL after successful update."""
        messages.add_message(self.request, messages.SUCCESS, "Profile updated!")
        return reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)