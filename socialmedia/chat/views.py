from chat.models import Conversation, Message
from django.views.generic import DetailView, ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden, HttpResponseRedirect
from chat.mixins import UserIsParticipantMixin
from chat.forms import MessageForm


class ConversationDetailView(LoginRequiredMixin, UserIsParticipantMixin, DetailView):
    model = Conversation
    template_name = "chat/conversation_detail.html"


class ConversationListView(LoginRequiredMixin, ListView):
    model = Conversation
    paginate_by = 100
    template_name = "chat/conversation_list.html"

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        user = self.request.user
        return qs.filter(participants__pk=user.pk)


@login_required
def send_message(request, conversation_pk):
    conversation = get_object_or_404(Conversation, pk=conversation_pk)
    if not conversation.participants.filter(pk=request.user.pk).exists():
        return HttpResponseForbidden("Not a participant of this conversation.")
    form = MessageForm(request.POST)
    message = form.instance
    message.author = request.user
    message.conversation = conversation
    if form.is_valid():
        form.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
