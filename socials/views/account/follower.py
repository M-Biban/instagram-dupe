from django.contrib.auth.mixins import LoginRequiredMixin
from socials.views.mixins import UserObjectAuthentication
from django.views.generic import DeleteView
from socials.models import Follower
from django.contrib import messages
from django.urls import reverse
from django.core.exceptions import PermissionDenied


class DeleteFollowerView(LoginRequiredMixin, UserObjectAuthentication, DeleteView):
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