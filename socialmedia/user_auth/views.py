from django.views.generic import DetailView, CreateView
from django.http import HttpResponseRedirect
from django.contrib.auth import login
from django.urls import reverse_lazy
from .models import User
from .forms import CustomUserCreationForm
from socialmedia.settings import LOGIN_REDIRECT_URL


class ProfileView(DetailView):
    model = User
    template_name = 'profile/profile.html'


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "registration/register.html"

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return HttpResponseRedirect(reverse_lazy(LOGIN_REDIRECT_URL))
