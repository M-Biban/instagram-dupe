from socials.models import Post, Image
from django import forms
from django.utils import timezone

class PostForm(forms.ModelForm):
    """Form to update user profiles."""

    class Meta:
        """Form options."""

        model = Post
        fields = ['caption']
        
    def save(self, user):
        Post.objects.create(
            caption = self.cleaned_data.get('caption'),
            user = user,
            created_at = timezone.now()
        )
        
class ImageForm(forms.ModelForm):
    """Form to update user profiles."""

    class Meta:
        """Form options."""

        model = Image
        fields = ['image']
        
    def save(self,post):
        Image.objects.create(
            post = post,
            image = self.cleaned_data.get('image')
        )