from django.views.generic import DetailView
from .models import Community
from django.db.models import Count


class CommunityView(DetailView):
    model = Community
    template_name = 'community/community_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = self.get_object().posts.all().annotate(
            number_of_likes=Count('likes'),
            number_of_dislikes=Count('dislikes'),
            number_of_comments=Count('comments')
        )
        return context
