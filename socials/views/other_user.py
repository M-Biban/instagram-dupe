from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, CreateView, View
from socials.models import User, Follower, FollowRequest
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied, ValidationError
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

class ViewUserView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'other_users/view_user.html'
    
    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()
        following = Follower.objects.filter(follower = request.user).values_list('user', flat=True)
        if object == request.user:
            return HttpResponseRedirect(reverse('view-profile'))
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        profile_user = self.get_object()  # The user whose profile is being viewed
        context['profile_user'] = profile_user
        context['user_followers'] = Follower.objects.filter(user = profile_user)
        context['user_is_following'] = Follower.objects.filter(follower = profile_user)
        context['following_user_list']= Follower.objects.filter(follower=self.request.user).values_list('user', flat=True)
        context['follower_user_list']= Follower.objects.filter(user=self.request.user).values_list('follower', flat=True)
        context['user'] = self.request.user
        context['follow_requests_made'] = FollowRequest.objects.filter(from_user = self.request.user).values_list('to_user', flat=True)
        
        return context
    
@login_required
def create_follow_request(request, pk):
    if request.method == "POST":
        user_to_follow = get_object_or_404(User, pk=pk)
        try:
            FollowRequest.objects.create(
                from_user = request.user,
                to_user = user_to_follow
            )
            messages.success(request, f'Follow request sent to {user_to_follow.username}')
        except ValidationError as e:
            messages.error(request, str(e))
    else:
        messages.warning(request, "Invalid request method.")
            
    return redirect(request.META.get('HTTP_REFERER', reverse('dashboard')))
    
    
@login_required
def accept_follow_request(request, pk):
    if request.method == 'POST':
        follow_request = get_object_or_404(FollowRequest, pk=pk)
        if follow_request.to_user != request.user:
            raise PermissionDenied("You cannot access this page as you're not logged in as the correct user.")
        follow_request.accept_request()
    else:
        messages.warning(request, "Invalid request method.")
    return redirect(request.META.get('HTTP_REFERER', reverse('dashboard')))

@login_required
def remove_follow_request(request, pk):
    if request.method == 'POST':
        follow_request = get_object_or_404(FollowRequest, pk=pk)
        if follow_request.to_user != request.user and follow_request.from_user != request.user:
            raise PermissionDenied("You cannot access this page as you're not logged in as the correct user.")
        follow_request.decline_request()
    else:
        messages.warning(request, "Invalid request method.")
    return redirect(request.META.get('HTTP_REFERER', reverse('dashboard')))