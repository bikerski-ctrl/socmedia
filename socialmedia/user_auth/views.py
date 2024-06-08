from django.views.generic import DetailView
from .models import User


class ProfileView(DetailView):
    model = User
    template_name = 'profile/profile.html'
