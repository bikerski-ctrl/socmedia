from django.views.generic import DetailView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden, HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.db.models import Count

from posts.models import Post, Comment
from community.models import Community
from posts.forms import PostForm, CommentForm
from posts.mixins import UserIsOwnerOrAdminMixin


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


class CommentUpdateView(LoginRequiredMixin, UserIsOwnerOrAdminMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "comments/comment_update.html"

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.post.pk})
    
    def form_valid(self, form):
        form.instance.edited = True
        return super().form_valid(form)



class CommentDeleteView(LoginRequiredMixin, UserIsOwnerOrAdminMixin, DeleteView):
    model = Comment
    template_name = "comments/comment_delete_confirmation.html"

    def get_success_url(self):
        return reverse_lazy("post_detail", kwargs={'pk':self.object.post.pk})


def save_post_with_author(form, user):
    post = form.instance
    post.author = user
    if form.is_valid():
        form.save()


@login_required
@require_POST
def create_post(request):
    form = PostForm(request.POST, request.FILES)
    save_post_with_author(form, request.user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
@require_POST
def create_community_post(request, community_pk):
    form = PostForm(request.POST, request.FILES)
    post = form.instance
    community = get_object_or_404(Community, pk=community_pk)
    if not community.is_allowed_to_post(request.user):
        return HttpResponseForbidden("Not allowed to post in this community.")
    post.community = community
    save_post_with_author(form, request.user)
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

@login_required
def react_post_comment(request, instance, action, pk):
    if instance == "post":
        obj = get_object_or_404(Post, pk=pk)
    elif instance == "comment":
        obj = get_object_or_404(Comment, pk=pk)
    else:
        return HttpResponseBadRequest()
    
    if action == "like":
        obj.like(request.user)
    elif action == "dislike":
        obj.dislike(request.user)
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
