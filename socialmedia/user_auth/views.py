from django.views.generic import DetailView, CreateView
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponseForbidden
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
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
