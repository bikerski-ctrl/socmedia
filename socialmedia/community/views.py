from django.views.generic import DetailView
from .models import Community
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import CommunityForm
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect


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


@login_required
@require_POST
def create_community(request):
    form = CommunityForm(request.POST, request.FILES)
    community = form.instance
    community.administrator = request.user
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse_lazy('community_detail', pk=community.pk))
    return HttpResponseBadRequest("Bad form.")
