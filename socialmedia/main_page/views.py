from django.shortcuts import render
from django.views.generic import ListView
from posts.models import Post
from django.db.models import Q
from posts.models import Post


def get_unauth_main_page(request):
    return render(request, "unauth_main_page.html")

class MainPageView(ListView):
    model = Post
    template_name = "auth_main_page.html"
    paginate_by = 20

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            Q(author__subscribers__pk=user.pk) | 
            Q(author__friends__pk=user.pk) | 
            Q(community__followers__pk=user.pk)
        ).order_by("-posted_at")
        return qs
    
    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return get_unauth_main_page(self.request)
        return super().get(*args, **kwargs)
