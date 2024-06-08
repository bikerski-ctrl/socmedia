from django.urls import path
from .views import ProfileView, RegisterView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register', RegisterView.as_view(), name="register"),
    path('logout', LogoutView.as_view(), name="logout"),

    # MUST BE KEPT LAST
    path('<str:pk>', ProfileView.as_view(), name="profile"),
]
