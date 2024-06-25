from django.urls import path
import posts.views as v

urlpatterns = [
    path('create/', v.post, name="post_create"),
    path('<int:pk>/', v.PostDetailView.as_view(), name="post_detail"),
    path('<int:pk>/update/', v.PostUpdateView.as_view(), name="post_update"),
    path('<int:pk>/delete/', v.PostDeleteView.as_view(), name="post_delete"),
    path('<int:post_pk>/comment', v.post_comment, name="comment_create")
]
