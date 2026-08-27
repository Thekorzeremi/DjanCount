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

def event_detail_view(request):
    #MOCK a remplacer avec logique model
    participants = ["Julie", "Seer", "Conambot", "Rémi"]
    
    expenses = [
        {"title": "Pizzas", "amount": 60.0, "payer": "Julie"},
        {"title": "Boissons", "amount": 20.0, "payer": "Rémi"},
        {"title": "Essence", "amount": 40.0, "payer": "Seer"},
    ]

    total_expenses = 0
    balances = {} 

    for expense in expenses:
        total_expenses += expense["amount"]
    
    part_per_pe = 0
    if len(participants) > 0:
        part_per_pe = total_expenses / len(participants)
    
    for participant in participants:
        balances[participant] = -part_per_pe
    
    for expense in expenses:
        payer = expense["payer"]
        if payer in balances: 
            balances[payer] += expense["amount"]

    transactions = []
    debt = []
    initier = []

    for name, sold in balances.items():
        if sold < -0.01:
            debt.append([name, -sold])
        elif sold > 0.01:
            initier.append([name, sold])

    i = 0
    j = 0

    while i < len(debt) and j < len(initier):
        amount_paid = min(debt[i][1], initier[j][1])
        
        transactions.append({
            'from': debt[i][0],
            'to': initier[j][0],
            'amount': round(amount_paid, 2)
        })
        
        debt[i][1] -= amount_paid
        initier[j][1] -= amount_paid
        
        if debt[i][1] <= 0.01:
            i += 1
        if initier[j][1] <= 0.01:
            j += 1

    context = {
        'participants': participants,
        'expenses': expenses,
        'total': total_expenses,
        'part': part_per_pe,
        'balances': balances,
        'transactions': transactions
    }

    return render(request, 'expenses/event_detail.html', context)