from django.db.models import Q
from django.shortcuts import render
from rest_framework import viewsets
from .models import Event, Expense
from .serializers import EventSerializer, ExpenseSerializer
from .permissions import IsEventParticipant, IsPayerOrEventParticipant

# ==============================================================================
# 📡 VUES API REST (Membre 2 - Django REST Framework)
# ==============================================================================

class EventViewSet(viewsets.ModelViewSet):
    """
    ViewSet d'API REST pour la ressource Event.
    Fournit automatiquement toutes les méthodes CRUD :
    - GET    /api/events/      -> Liste des événements (List)
    - POST   /api/events/      -> Création d'un événement (Create)
    - GET    /api/events/{id}/ -> Détail d'un événement (Retrieve)
    - PUT    /api/events/{id}/ -> Modification complète (Update)
    - PATCH  /api/events/{id}/ -> Modification partielle (Partial Update)
    - DELETE /api/events/{id}/ -> Suppression (Destroy)
    """
    queryset = Event.objects.prefetch_related("participants", "expenses").all()
    serializer_class = EventSerializer
    permission_classes = [IsEventParticipant]

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset
        return self.queryset.filter(participants=self.request.user).distinct()


class ExpenseViewSet(viewsets.ModelViewSet):
    """
    ViewSet d'API REST pour la ressource Expense.
    Fournit automatiquement toutes les méthodes CRUD :
    - GET    /api/expenses/      -> Liste de toutes les dépenses (List)
    - POST   /api/expenses/      -> Création d'une nouvelle dépense (Create)
    - GET    /api/expenses/{id}/ -> Détail d'une dépense (Retrieve)
    - PUT    /api/expenses/{id}/ -> Modification complète (Update)
    - PATCH  /api/expenses/{id}/ -> Modification partielle (Partial Update)
    - DELETE /api/expenses/{id}/ -> Suppression (Destroy)
    """
    queryset = Expense.objects.select_related("payer", "event").all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsPayerOrEventParticipant]

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset
        return self.queryset.filter(
            Q(payer=self.request.user) | Q(event__participants=self.request.user)
        ).distinct()


# ==============================================================================
# 🖼️ VUE WEB HTML (Membre 4)
# ==============================================================================

# TODO: Membre 4 - Vue HTML event_detail_view(request, event_id)
