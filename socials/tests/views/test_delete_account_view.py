"""Unit tests for Delete Account View"""
from django.test import TestCase
from django.urls import reverse
from socials.models import User
from socials.forms import ConfirmPasswordForm

class AccountDeleteViewTestCase(TestCase):
    """Unit tests for Delete Account View"""
    
    fixtures = [
        'socials/tests/fixtures/default_user.json',
    ]
    
    def setUp(self):
        self.user = User.objects.get(username = 'johndoe')
        self.url = reverse('delete-profile')
        self.form_input = {
            'password' : 'Password123'
        }
        
    def test_delete_account_url(self):
        self.assertEqual(self.url,'/delete-profile/')
    
    def test_view_deletes_user(self):
        self.client.login(username = self.user.username, password='Password123')
        response = self.client.post(self.url, self.form_input, follow=True)
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())  # Check that the task is deleted
        
    def test_correct_template(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'account/delete-profile.html')
        
    def test_correct_form_class(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        form = response.context['form']
        self.assertTrue(isinstance(form, ConfirmPasswordForm))
        
    def test_incorrect_input(self):
        self.form_input['password'] = "WrongPassword123"
        self.client.login(username = self.user.username, password='Password123')
        response = self.client.post(self.url, self.form_input, follow=True)
        self.assertTrue(User.objects.filter(pk=self.user.pk).exists()) 
    
    def test_view_redirect(self):
        self.client.login(username = self.user.username, password='Password123')
        response = self.client.post(self.url, self.form_input, follow=True)
        redirect_url = reverse('home')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        