from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Follower, Friendship

@receiver(post_save, sender=Follower)
def create_friendship_if_both_follow(sender, instance, created, **kwargs):
    if created:  # Check if the Follower instance is newly created
        follower = instance.follower
        followee = instance.current_user

        # Check if the followee also follows the follower
        if Follower.objects.filter(follower=followee, current_user=follower).exists():
            # Create a friendship if they are not already friends
            Friendship.objects.get_or_create(user1=min(follower, followee, key=lambda x: x.id),
                                             user2=max(follower, followee, key=lambda x: x.id))
