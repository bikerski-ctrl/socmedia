from django.urls import path
import community.views as v

urlpatterns = [
    path('<int:pk>/', v.CommunityView.as_view(), name="community_detail"),
    path('create/', v.CreateCommunityView.as_view(), name="community_create"),
    path('list/', v.CommunityListView.as_view(), name="community_list"),
]