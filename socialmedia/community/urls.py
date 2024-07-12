from django.urls import path
import community.views as v

urlpatterns = [
    path('community/<int:pk>/', v.CommunityView.as_view(), name="community_detail"),
]