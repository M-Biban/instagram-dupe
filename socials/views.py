# socials/views.py
from django.shortcuts import render, redirect
from django.views.generic import FormView, View, UpdateView, DeleteView, ListView
from django.contrib.auth import login, logout
from .forms import SignUpForm, LogInForm, ConfirmPasswordForm, UserForm
from .models import User, Follower
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from socials.helpers import login_prohibited
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q 
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

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
        
class UserObjectAuthentication:
    """Mixin that raises permission denied if the user tries to access an object they are not the owner of"""
    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()
        if object.user != request.user:
            raise PermissionDenied("You cannot access this page as you're not logged in as the correct user.")
        return super().dispatch(request, *args, **kwargs)

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
    return render(request, 'view-profile.html',{'user': request.user, 'followers': Follower.objects.filter(user = request.user), 'following':Follower.objects.filter(follower = request.user)})

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
    
    
    
class FollowerDeleteView(LoginRequiredMixin, UserObjectAuthentication, DeleteView):
    """View to delete followers"""
    
    model = Follower
    
    def get_object(self, queryset=None):
        """Get follower to be deleted"""
        follower_pk = self.kwargs.get('pk')
        follower = Follower.objects.get(pk=follower_pk)
        return follower
    
    def get_success_url(self):
        """Redirect to my_entries on successful form submission"""
        messages.add_message(self.request, messages.SUCCESS, "Follower deleted successfully!")
        return reverse('view-profile') 
    
class RemoveFollowerView(LoginRequiredMixin, DeleteView):
    model = Follower
    
    def get_object(self, queryset=None):
        """Get follower to be deleted"""
        follower_pk = self.kwargs.get('pk')
        follower = Follower.objects.get(pk=follower_pk)
        return follower
    
    def get_success_url(self):
        """Redirect to my_entries on successful form submission"""
        messages.add_message(self.request, messages.SUCCESS, "Follower removed successfully!")
        return reverse('view-profile') 
    
    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()
        if object.follower != request.user:
            raise PermissionDenied("You cannot access this page as you're not logged in as the correct user.")
        return super().dispatch(request, *args, **kwargs)
    
@csrf_exempt    
def search_view(request):
    query = request.GET.get('query', '')
    results = []
    
    if query:
        results = User.objects.filter(Q(username__icontains=query) | Q(first_name__icontains=query)  | Q(last_name__icontains=query)).values('id', 'first_name', 'profile_pic', 'username')
        
    results = list(results)
        
    for result in results:
        result['profile_pic'] = settings.MEDIA_URL + result['profile_pic']
        
    return JsonResponse({'results': list(results)})    
    