"""Context processor for friends"""
from socials.models import User, Friendship

def friends_processor(request):
    """Returns the number of badges the user has earned"""
    friends = []
    if request.user.is_authenticated:
        friends1 = Friendship.objects.filter(user1 = request.user).values_list('user2', flat=True)
        friends2 = Friendship.objects.filter(user2 = request.user).values_list('user1', flat=True)
        ids = []
        for t in friends1:
            ids.append(t)
        for t in friends2:
            ids.append(t)
        friends = User.objects.filter(id__in=ids) 
    return {"friends": friends}