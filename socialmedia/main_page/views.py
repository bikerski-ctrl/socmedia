from django.shortcuts import render
from django.views.generic import ListView
from posts.models import Post
from django.db.models import Q, Count
from posts.models import Post


def get_unauth_main_page(request):
    return render(request, "unauth_main_page.html")

class MainPageView(ListView):
    model = Post
    template_name = "auth_main_page.html"
    paginate_by = 20

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        user = self.request.user
        qs = qs.filter(
            Q(author__subscribers__subscriber=user) | 
            Q(author__friends=user) | 
            Q(community__follower=user)
        ).order_by("-posted_at").annotate(
            number_of_likes=Count('likes'),
            number_of_dislikes=Count('dislikes'),
            number_of_comments=Count('comments')
        )
        return qs
    
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return get_unauth_main_page(self.request)

        super().get(request, *args, **kwargs)

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return render(request, 'main_list.html', context=self.get_context_data())

        return render(request, self.template_name, context=self.get_context_data())
