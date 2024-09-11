from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.urls import reverse
from socials.forms import PostForm, ImageForm
from django.contrib import messages
from socials.models import Post, Image
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from PIL import Image as PILImage
from io import BytesIO

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
    
    
def handleMultipleImagesUpload(request, pk):
    if request.method == "POST":
        images = request.FILES.getlist('images')
        post = get_object_or_404(Post, pk=pk)
        
        valid_images = []
        for image in images:
            # Check if the file is an image
            try:
                img = PILImage.open(image)
                img.verify()  # Verify that it is, in fact, an image
                valid_images.append(image)
            except (IOError, SyntaxError) as e:
                return JsonResponse({"error": "One or more files are not valid images"}, status=400)


        for image in valid_images:
            Image.objects.create(image = image, post = post)

        uploaded_images = Image.objects.all()
        return JsonResponse({"images": [{"url": image.image.url} for image in uploaded_images]})
    return render(request, "post/add_image.html")
