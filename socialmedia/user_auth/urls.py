from django.urls import path
from .views import ProfileView, RegisterView

urlpatterns = [
    path('register', RegisterView.as_view(), name="register"),
    path('<str:pk>', ProfileView.as_view(), name="profile"),
]
