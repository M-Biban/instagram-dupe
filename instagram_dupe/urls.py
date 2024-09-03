"""
URL configuration for instagram_dupe project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from socials import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('sign-up/', views.SignUpView.as_view(), name="sign-up"),
    path('log-in/', views.LogInView.as_view(), name="log-in"),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('log-out/', views.log_out, name='log-out'),
    path('view-profile/', views.view_profile, name='view-profile'),
    path('delete-profile/', views.DeleteProfileView.as_view(), name='delete-profile'),
    path('edit-profile/', views.EditProfileView.as_view(), name='edit-profile'),
    path('delete-follower/<int:pk>/', views.DeleteFollowerView.as_view(), name='delete-follower'),
    path('remove-follower/<int:pk>/', views.RemoveFollowerView.as_view(), name="remove-follower"),
    path('search/', views.search_view, name='search'),
    path('view_user/<int:pk>/', views.ViewUserView.as_view(), name='view_user'),
    path('create-follow-request/<int:pk>/', views.create_follow_request, name="create-follow-request")
]

urlpatterns += static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )