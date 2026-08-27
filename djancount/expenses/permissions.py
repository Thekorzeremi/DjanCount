"""Permissions métier propres aux ressources de l'application expenses."""

from rest_framework.permissions import IsAuthenticated


class IsEventParticipant(IsAuthenticated):
    """Réserve un événement à ses participants et aux administrateurs."""

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.participants.filter(pk=request.user.pk).exists()


class IsPayerOrEventParticipant(IsAuthenticated):
    """Réserve une dépense à son payeur, aux participants de l'événement ou au staff."""

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_staff
            or obj.payer_id == request.user.pk
            or obj.event.participants.filter(pk=request.user.pk).exists()
        )
