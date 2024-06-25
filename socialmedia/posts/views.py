from django.views.generic import DetailView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden, HttpResponseBadRequest
from posts.forms import PostForm, CommentForm
from posts.models import Post, Comment
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from posts.mixins import UserIsOwnerOrAdminMixin
from django.shortcuts import get_object_or_404
from django.db.models import Count


class PostDetailView(DetailView):
    model = Post
    template_name = "posts/post.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.object
        obj.number_of_likes = obj.likes.count()
        obj.number_of_dislikes = obj.dislikes.count()
        context["object"] = obj
        context.update(kwargs)
        context["comments"] = self.object.comments.annotate(
            number_of_likes=Count('likes'),
            number_of_dislikes=Count('dislikes'),
        )
        return context


class PostUpdateView(LoginRequiredMixin, UserIsOwnerOrAdminMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "posts/post_update.html"

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.edited = True
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, UserIsOwnerOrAdminMixin, DeleteView):
    model = Post
    template_name = "posts/post_delete_confirmation.html"

    def get_success_url(self):
        return reverse_lazy('main_page')


@login_required
def post(request):
    if request.method.lower() != "post":
        return HttpResponseForbidden("Only POST requests are allowed.")
    form = PostForm(request.POST, request.FILES)
    post = form.instance
    post.author = request.user
    if form.is_valid():
        form.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def post_comment(request, post_pk):
    if request.method.lower() != "post":
        return HttpResponseForbidden("Only POST requests are allowed.")
    post = get_object_or_404(Post, pk=post_pk)

    form = CommentForm(request.POST, request.FILES)
    comment = form.instance
    comment.author = request.user
    comment.post = post

    if form.is_valid():
        comment.save()
    url = reverse_lazy("post_detail", kwargs={'pk': post.pk})
    return HttpResponseRedirect(url)
