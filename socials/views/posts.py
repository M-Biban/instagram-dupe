from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.views.generic import DetailView
from django.urls import reverse
from django.core.exceptions import PermissionDenied, ValidationError
from socials.forms import PostForm
from django.contrib import messages
from socials.models import Post, Image
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from PIL import Image as PILImage
from io import BytesIO

class CreatePostView(LoginRequiredMixin, FormView):
    
    template_name = "post/create_post.html"
    form_class = PostForm
    
    def get_user(self):
        return self.request.user
        
    def form_valid(self, form):
        user = self.get_user()
        self.new_post = form.save(user=user)
        messages.success(self.request, "Post created!")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context
    
    def get_success_url(self):
        return reverse("add-image", kwargs={'pk': self.new_post.pk})
    
    
def handleMultipleImagesUpload(request, pk):
    if request.method == "POST":
        images = request.FILES.getlist('images')
        post = get_object_or_404(Post, pk=pk)
        
        if post.user == request.user:
            valid_images = []
            for image in images:
                # Check if the file is an image
                try:
                    img = PILImage.open(image)
                    img.verify()  # Verify that it is, in fact, an image
                    valid_images.append(image)
                except (IOError, SyntaxError) as e:
                    return ValidationError("one or more of your uploaded files are not images")


            for image in valid_images:
                Image.objects.create(image = image, post = post)

            uploaded_images = Image.objects.all()
            return HttpResponseRedirect(reverse("confirm-post", kwargs={'pk': post.pk}))
        else:
            raise PermissionDenied("You are not the user of this post")
    return render(request, "post/add_image.html")

class ConfirmPostView(LoginRequiredMixin, DetailView):
    
    model = Post
    template_name = 'post/confirm_post.html'
    
    def get_object(self, queryset=None):
        post_pk = self.kwargs.get('pk')
        post = Post.objects.get(pk=post_pk)
        return post
    
    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if post.user != request.user:
            raise PermissionDenied("You are not the user of this post")
        if not post.draft:
            raise PermissionDenied("this post was already posted")
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
         post = self.get_object()
         
         context['post'] = post
         context['images'] = Image.objects.filter(post = post)
         return context
     
def publishPost(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    if post.user != request.user:
        raise PermissionDenied("You are not the user of this post")
    
    if request.method == "POST":
        if post.draft:
            post.not_draft()
            messages.success(request, "Post pubished!")
            return HttpResponseRedirect(reverse("view-profile"))
        else:
            messages.error(request, "This is not allowed")
            return redirect("view-profile")

    return redirect("view-profile")
            