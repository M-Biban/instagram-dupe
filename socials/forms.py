from .models import User
from django import forms

class UserForm(forms.ModelForm):
    """Form to update user profiles."""

    class Meta:
        """Form options."""

        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
        
class SignUpForm(forms.ModelForm):
    
    class Meta:
        """Form options"""
        
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
        
    def save(self):
        """Create new user"""
        
        super().save(commit=False)
        user = User.objects.create(
            username = self.cleaned_data.get('username'),
            first_name = self.cleaned_data.get('first_name'),
            last_name = self.cleaned_data.get('last_name'),
            email = self.cleaned_data.get('email'),
        )
        
        return user