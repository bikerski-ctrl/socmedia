from chat.models import Conversation, Message
from django.views.generic import DetailView, ListView


class ConversationDetailView(DetailView):
    model = Conversation
    template_name = "chat/conversation_detail.html"


class ConversationListView(ListView):
    model = Conversation
    paginate_by = 100
    template_name = "chat/conversation_list.html"
