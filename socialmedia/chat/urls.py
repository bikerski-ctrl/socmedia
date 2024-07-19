from django.urls import path
import chat.views as v

urlpatterns = [
    path("list/", v.ConversationListView.as_view(), name="conversation_list"),
    path("<int:pk>/", v.ConversationDetailView.as_view(), name="conversation_detail"),
    path("<int:conversation_pk>/send", v.send_message, name="send_message"),
]