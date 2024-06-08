from django.urls import path
from .views import ProfileView

urlpatterns = [
    path('<str:pk>', ProfileView.as_view(), name="profile"),
]
