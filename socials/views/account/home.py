from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from socials.helpers import login_prohibited

@login_prohibited
def home(request):
    return render(request, 'home.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html',{'user': request.user})