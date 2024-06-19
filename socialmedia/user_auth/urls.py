from django.urls import path
from .views import ProfileView, RegisterView, SubscriptionView, FriendRequestView, update_user_status, update_user_description, unfriend_user
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),

    # MUST BE KEPT LAST
    path('<str:pk>/', ProfileView.as_view(), name="profile"),
    path('<str:pk>/status_update/', update_user_status, name="change_status"),
    path('<str:pk>/change_description/', update_user_description, name="change_description"),
    path('<str:pk>/subscription/<str:action>', SubscriptionView.as_view(), name="subscription"),
    path('<str:pk>/friend_request/<str:action>', FriendRequestView.as_view(), name="friend_request"),
    path('<str:pk>/unfriend', unfriend_user, name="unfriend"),
]
