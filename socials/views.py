from django.shortcuts import render
from django.views.generic.edit import FormView, UpdateView
from socials.forms import UserForm, SignUpForm
from django.urls import reverse
from django.contrib.auth import login, logout

# Create your views here.
def home(request):
    
    return render(request, 'home.html')
    
class UserFormView(FormView):
    
    template_name = "user.html"
    form_class = UserForm

    def get_object(self):
        """Return the object (user) to be updated."""
        user = self.request.user
        return user

    def get_success_url(self):
        return reverse('home')
    
class SignUpView(FormView):
    
    form_class = SignUpForm
    template_name = "sign-up.html"
    
    def form_valid(self, form):
        self.object = form.save()
        login(self.request, self.object)
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('home')