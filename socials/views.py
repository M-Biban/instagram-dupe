# socials/views.py
from django.shortcuts import render, redirect
from django.views.generic import FormView, View
from django.contrib.auth import login, logout
from .forms import SignUpForm, LogInForm
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from socials.helpers import login_prohibited
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured, PermissionDenied

@login_prohibited
def home(request):
    return render(request, 'home.html')

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

    def get_success_url(self):
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
        return redirect(reverse('log-in'))

    def get_success_url(self):
        return reverse(self.redirect_when_logged_in_url)
    

@login_required
def log_out(request):
    """Log out the current user"""

    logout(request)
    return redirect('home')


