from django.urls import path
from .views import ProfileView, RegisterView, update_user_status
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),

    # MUST BE KEPT LAST
    path('<str:pk>/', ProfileView.as_view(), name="profile"),
    path('<str:pk>/status_update/', update_user_status, name="change_status"),
]
