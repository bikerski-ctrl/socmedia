from django.views.generic import DetailView, UpdateView
from django.contrib.auth.decorators import login_required
from posts.forms import PostForm, CommentForm
from posts.models import Post, Comment
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect


class PostDetailView(DetailView):
    model = Post
    template_name = "posts/post.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = self.object.comments
        return context


class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = "posts/update_post.html"

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.pk})


@login_required
def post(request):
    form = PostForm(request.POST, request.FILES)
    form.instance.author = request.user
    if form.is_valid():
        form.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
