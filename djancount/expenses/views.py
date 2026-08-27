from django.db.models import Q
from django.shortcuts import render, get_object_or_404
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

def event_detail_view(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    participants = list(event.participants.all())
    expenses = event.expenses.select_related("payer").all()

    total_expenses = sum(expense.amount for expense in expenses)
    part_per_person = total_expenses / len(participants) if participants else 0

    balances = {}
    for participant in participants:
        balances[participant.first_name] = -part_per_person

    for expense in expenses:
        payer_name = expense.payer.first_name
        if payer_name in balances:
            balances[payer_name] += expense.amount

    transactions = []
    debtors = []
    creditors = []

    for name, balance in balances.items():
        if balance < -0.01:
            debtors.append([name, -balance])
        elif balance > 0.01:
            creditors.append([name, balance])

    i = 0
    j = 0

    while i < len(debtors) and j < len(creditors):
        amount = min(debtors[i][1], creditors[j][1])

        transactions.append({
            'from': debtors[i][0],
            'to': creditors[j][0],
            'amount': round(amount, 2)
        })

        debtors[i][1] -= amount
        creditors[j][1] -= amount

        if debtors[i][1] <= 0.01:
            i += 1
        if creditors[j][1] <= 0.01:
            j += 1

    context = {
        'event': event,
        'participants': participants,
        'expenses': expenses,
        'total': total_expenses,
        'part': part_per_person,
        'balances': balances,
        'transactions': transactions
    }

    return render(request, 'expenses/event_detail.html', context)