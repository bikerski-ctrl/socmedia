from django.urls import path
import posts.views as v

urlpatterns = [
    path('<int:pk>', v.PostDetailView.as_view(), name="post_detail"),
    path('<int:pk>/update', v.PostUpdateView.as_view(), name="post_update"),
    path('<int:pk>/delete', v.PostDeleteView.as_view(), name="post_delete"),
]
