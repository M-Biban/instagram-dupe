from django.core.management.base import BaseCommand, CommandError
from socials.models import User, Follower, Friendship, FollowRequest

class Command(BaseCommand):
    """Build automation command to unseed the database."""
    
    help = 'Seeds the database with sample data'

    def handle(self, *args, **options):
        """Unseed the database."""

        User.objects.filter(is_staff=False).delete()
        Follower.objects.filter().delete()
        Friendship.objects.filter().delete()
        FollowRequest.objects.filter().delete()