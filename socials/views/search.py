from django.views.decorators.csrf import csrf_exempt
from socials.models import User
from django.conf import settings
from django.http import JsonResponse
from django.db.models import Q 

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