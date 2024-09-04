from socials.forms import SignUpForm, LogInForm
from socials.views.mixins import LoginProhibitedMixin
from django.views.generic import FormView
from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

class SignUpView(LoginProhibitedMixin, FormView):
    form_class = SignUpForm
    template_name = "account/sign-up.html"
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
    template_name = "account/log-in.html"
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
