from django.core.exceptions import PermissionDenied


class UserIsParticipantMixin():
    def dispatch(self, request, *args, **kwargs):
        instance = self.get_object()
        user = self.request.user
        if not instance.participants.filter(pk=user.pk).exists():
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)