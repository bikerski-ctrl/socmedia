from django.views.generic import DetailView, CreateView, View
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponseForbidden
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from .models import User
from .forms import CustomUserCreationForm
from django.conf import settings


class ProfileView(DetailView):
    model = User
    template_name = 'profile/profile.html'


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "registration/register.html"

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)


class SubscriptionView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        subscriber = request.user
        user = get_object_or_404(User, pk=request.pk)
        subscriber.subscribe(user)

    def delete(self, request, *args, **kwargs):
        pass


class FriendRequestView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        pass


@login_required
def update_user_status(request, pk):
    if request.method != "POST":
        return HttpResponseBadRequest("Unable to process this request.")
    user = request.user
    if pk != user.pk:
        return HttpResponseForbidden("This action is not allowed.")
    new_status = request.POST.get("status")
    user.status = new_status
    user.save()
    return HttpResponseRedirect(reverse_lazy(
        "profile", kwargs={'pk': user.pk}
    ))


# duplicate code: optimize?
@login_required
def update_user_description(request, pk):
    if request.method != "POST":
        return HttpResponseBadRequest("Unable to process this request.")
    user = request.user
    if pk != user.pk:
        return HttpResponseForbidden("This action is not allowed.")
    new_description = request.POST.get("description")
    user.description = new_description
    user.save()
    return HttpResponseRedirect(reverse_lazy(
        "profile", kwargs={'pk': user.pk}
    ))


@login_required
def unfriend(request, pk):
    pass
