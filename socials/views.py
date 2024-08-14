# socials/views.py
from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.contrib.auth import login
from .forms import SignUpForm, LogInForm
from django.urls import reverse

def home(request):
    return render(request, 'home.html')

class SignUpView(FormView):
    form_class = SignUpForm
    template_name = "sign-up.html"

    def form_valid(self, form):
        self.object = form.save()
        login(self.request, self.object)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('home')

class LogInView(FormView):
    form_class = LogInForm
    template_name = "log-in.html"

    def form_valid(self, form):
        login(self.request, form.get_user())
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('home')
