from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Follower, Friendship, FollowRequest

@receiver(post_save, sender=Follower)
def create_friendship_if_both_follow(sender, instance, created, **kwargs):
    if created:  # Check if the Follower instance is newly created
        follower = instance.follower
        followee = instance.user

        # Check if the followee also follows the follower
        if Follower.objects.filter(follower=followee, user=follower).exists():
            # Create a friendship if they are not already friends
            Friendship.objects.get_or_create(user1=min(follower, followee, key=lambda x: x.id),
                                             user2=max(follower, followee, key=lambda x: x.id))
            
@receiver(post_save, sender=FollowRequest)
def automatic_follow(sender, instance, created, **kwargs):
    if created: #Check if the FollowRequest instance is newly created
        from_user = instance.from_user
        to_user = instance.to_user
        
        if to_user.private == False:
            instance.accept_request()
            
@receiver(post_delete, sender=Follower)
def delete_friendship_if_follower_removed(sender, instance, **kwargs):
    user1 = instance.follower
    user2 = instance.user
        
    if Friendship.objects.filter(user1=user1, user2=user2).exists():
        Friendship.objects.get(user1=user1, user2=user2).delete()
    if Friendship.objects.filter(user1=user2, user2=user1).exists():
        Friendship.objects.get(user1=user2, user2=user1).delete()
