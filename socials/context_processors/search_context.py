from socials.models import User
from django.db.models import Q

def search(request):
    query = request.GET.get("q")
    if query is not None:
        object_list = User.objects.filter(
            Q(username__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query)
            )
        return object_list
    else:
        return []