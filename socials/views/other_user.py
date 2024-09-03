from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from socials.models import User, Follower
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.urls import reverse

class ViewUserView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'view_user.html'
    
    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()
        following = Follower.objects.filter(follower = request.user).values_list('user', flat=True)
        if object == request.user:
            return HttpResponseRedirect(reverse('view-profile'))
        if object.private and object.pk not in following:
            raise PermissionDenied("You cannot access this page as you're not logged in as the correct user.") #probs change this to something more relevant
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        profile_user = self.get_object()  # The user whose profile is being viewed
        context['profile_user'] = profile_user
        context['user_followers'] = Follower.objects.filter(user = profile_user)
        context['user_is_following'] = Follower.objects.filter(follower = profile_user)
        
        return context