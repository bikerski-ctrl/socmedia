from django.views.generic import DetailView, View, ListView
from django.shortcuts import render
from .models import Community
from django.db.models import Count
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CommunityForm
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator


class CommunityView(DetailView):
    model = Community
    template_name = 'community/community_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = self.get_object().posts.all().order_by("-posted_at").annotate(
            number_of_likes=Count('likes'),
            number_of_dislikes=Count('dislikes'),
            number_of_comments=Count('comments')
        )
        paginator = Paginator(posts, 20)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context["posts"] = page_obj
        return context
    
    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return render(request, 'community/community_post_list.html', context=self.get_context_data())
        return render(request, self.template_name, context=self.get_context_data())


class CreateCommunityView(LoginRequiredMixin, View):
    def post(self, request):
        form = CommunityForm(request.POST, request.FILES)
        community = form.instance
        community.administrator = request.user
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse_lazy('community_detail', kwargs={'pk':community.pk}))
        return HttpResponseBadRequest("Bad form.")
    
    def get(self, request):
        return render(request, "community/community_create.html")


class CommunityListView(ListView):
    model = Community
    template_name = "community/community_list.html"
    paginate_by = 20

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.annotate(
            followers=Count('follower')
        )
        return qs.order_by('followers')