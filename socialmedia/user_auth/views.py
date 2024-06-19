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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        viewer = self.request.user
        viewed_user = self.get_object()
        if viewer.is_authenticated:
            context["subscribed"] = viewer.is_subscribed_to(viewed_user)
            context["is_friends"] = viewer.is_friends(viewed_user)
            context["sent_friend_request"] = viewer.has_sent_friend_request(viewed_user)
            context["received_friend_request"] = viewer.has_received_friend_request(viewed_user)
        return context


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "registration/register.html"

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)


class SubscriptionView(LoginRequiredMixin, View):
    def post(self, request, pk, action, *args, **kwargs):
        if action == "delete":
            return self.delete(request, pk, *args, **kwargs)
        subscriber = request.user
        user = get_object_or_404(User, pk=pk)
        subscriber.subscribe(user)
        response_url = reverse_lazy("profile", kwargs={'pk': pk})
        return HttpResponseRedirect(response_url)

    def delete(self, request, pk, *args, **kwargs):
        subscription = get_object_or_404(request.user.subscriptions, subscribed_to__pk=pk)
        subscription.delete()
        response_url = reverse_lazy("profile", kwargs={'pk': pk})
        return HttpResponseRedirect(response_url)


class FriendRequestView(LoginRequiredMixin, View):
    def post(self, request, pk, action, *args, **kwargs):
        if action == "delete":
            self.delete(request, pk, *args, **kwargs)
        user = request.user
        send_to = get_object_or_404(User, pk=pk)
        user.send_friend_request(send_to)
        response_url = reverse_lazy("profile", kwargs={'pk': pk})
        return HttpResponseRedirect(response_url)

    def delete(self, request, pk, *args, **kwargs):
        user = request.user
        unsend_to = get_object_or_404(User, pk=pk)
        user.unsend_friend_request(unsend_to)
        response_url = reverse_lazy("profile", kwargs={'pk': pk})
        return HttpResponseRedirect(response_url)


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
def unfriend_user(request, pk):
    user = request.user
    to_unfriend = get_object_or_404(User, pk=pk)
    user.unfriend_user(to_unfriend)
    return HttpResponseRedirect(reverse_lazy(
        "profile", kwargs={'pk': to_unfriend.pk}
    ))
