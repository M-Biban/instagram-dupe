from socials.models import Post, Image, Comment
from django import forms
from django.utils import timezone

class PostForm(forms.ModelForm):
    """Form to update user profiles."""

    class Meta:
        """Form options."""

        model = Post
        fields = ['caption']
        
    def save(self, user):
        post = Post.objects.create(
            caption = self.cleaned_data.get('caption'),
            user = user,
            created_at = timezone.now()
        )
        return post
    
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
        
class CommentForm(forms.ModelForm):
    
    class Meta:
        
        model = Comment
        fields = ['comment']
        
    def save(self, post, user):
        Comment.objects.create(
            comment = self.cleaned_data.get('comment'),
            post = post,
            commented_by = user,
            comment_time = timezone.now()
        )
        