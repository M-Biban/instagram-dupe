from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.urls import reverse
from socials.forms import PostForm, ImageForm
from django.contrib import messages
from socials.models import Post

class CreatePostView(LoginRequiredMixin, FormView):
    
    template_name = "post/create_post.html"
    form_class = PostForm
    
    def get_user(self):
        return self.request.user
    
    def form_valid(self, form):
        user = self.get_user()
        form.save( user=user)
        messages.success(self.request, "Post created!")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context
    
    def get_success_url(self):
        return reverse("dashboard")
    
class AddImageView(LoginRequiredMixin, FormView):
    
    template_name = "post/add_image.html"
    form_class = ImageForm
    
    def get_post(self):
        post_pk = self.kwargs.get('pk')
        post = Post.objects.get(pk=post_pk)
        return post
    
    def form_valid(self, form):
        post = self.get_post()
        form.save(post=post)
        messages.success(self.request, "Image added!")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.get_post()
        context['form'] = self.get_form()
        return context
    
    def get_success_url(self):
        return reverse("dashboard")
