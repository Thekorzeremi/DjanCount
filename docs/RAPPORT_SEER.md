# Rapport Individuel de Contribution Technique - API REST & DRF

**Auteur :** Seer MENSAH ASSIAKOLEY  
**Projet :** DjanCount  
**Rôle & Spécialité :** Développement API REST, Sérialisation & Validation Métier (Django REST Framework)  

---

## 1. Vision & Périmètre d'Intervention

Dans le cadre du projet **DjanCount**, ma responsabilité principale a été de concevoir et d'implémenter l'ensemble de la **couche API REST** via Django REST Framework (DRF).

L'objectif de mon travail était d'exposer une API claire, hautement performante et sécurisée au niveau métier, capable de gérer les opérations CRUD sur les événements et les dépenses de groupe tout en garantissant la cohérence des données financières.

**Composants clés développés dans le dépôt :**
- **Sérialiseurs & DTO** : [`djancount/expenses/serializers.py`](../djancount/expenses/serializers.py)
- **Contrôleurs ViewSets & Requêtes ORM** : [`djancount/expenses/views.py`](../djancount/expenses/views.py)
- **Routage API REST** : [`djancount/expenses/urls.py`](../djancount/expenses/urls.py)
- **Requêtes Client HTTP de Test** : [`http-requests/`](../http-requests/)

---

## 2. Conception des Sérialiseurs & Validations Métiers

### A. Sérialisation Optimisée & Champs Calculés

Pour éviter au client HTTP ou au frontend d'avoir à multiplier les requêtes pour obtenir des informations annexes, j'ai enrichi les sérialiseurs de champs calculés en lecture seule (`read_only=True`) :

- **`EventSerializer`** : ajoute automatiquement `participants_count` et `expenses_count`.
- **`ExpenseSerializer`** : résout dynamiquement `payer_name` (`payer.username`) et `event_name` (`event.name`).

```python
class EventSerializer(serializers.ModelSerializer):
    participants_count = serializers.IntegerField(source="participants.count", read_only=True)
    expenses_count = serializers.IntegerField(source="expenses.count", read_only=True)

    class Meta:
        model = Event
        fields = [
            "id", "name", "description", "participants", 
            "participants_count", "expenses_count"
        ]
        read_only_fields = ["id"]
```

### B. Contrôle d'Intégrité & Validateurs Métiers

J'ai structuré la validation des dépenses sur deux niveaux pour garantir qu'aucune donnée incohérente ne puisse être enregistrée en base :

1. **Validation atomique de champ (`validate_amount`)** :
   Empêche la création ou la modification d'une dépense avec un montant nul ou négatif.
2. **Validation inter-champs croisée (`validate`)** :
   Vérifie impérativement que l'utilisateur indiqué comme payeur (`payer`) fait bien partie de la liste des participants inscrits à l'événement (`event.participants`).

```python
class ExpenseSerializer(serializers.ModelSerializer):
    payer_name = serializers.CharField(source="payer.username", read_only=True)
    event_name = serializers.CharField(source="event.name", read_only=True)

    class Meta:
        model = Expense
        fields = ["id", "title", "amount", "payer", "payer_name", "event", "event_name", "date"]
        read_only_fields = ["id", "date"]

    def validate_amount(self, value):
        """Règle métier 1 : Le montant doit être strictement supérieur à 0."""
        if value <= 0:
            raise serializers.ValidationError("Le montant doit être strictement positif.")
        return value

    def validate(self, attrs):
        """Règle métier 2 : Le payeur doit appartenir aux participants de l'événement."""
        payer = attrs.get('payer', getattr(self.instance, 'payer', None))
        event = attrs.get('event', getattr(self.instance, 'event', None))
        
        if event and payer and payer not in event.participants.all():
            raise serializers.ValidationError(
                {"payer": "Le payeur doit faire partie des participants de cet événement."}
            )
        return attrs
```

---

## 3. Performance ORM & Contrôle de Visibilité dans les ViewSets

### A. Résolution du Problème N+1 Requêtes SQL

Par défaut, l'accès aux relations d'un modèle lors de la sérialisation d'une liste déclenche une requête SQL par élément (problème N+1). Pour optimiser drastiquement les performances de la base de données SQLite :

- J'ai appliqué **`select_related("payer", "event")`** sur `ExpenseViewSet` pour forcer une jointure SQL `INNER JOIN` unique lors de la récupération des dépenses.
- J'ai appliqué **`prefetch_related("participants", "expenses")`** sur `EventViewSet` pour charger efficacement les relations N-N et les clés inverses.

### B. Isolation Granulaire des Données par Utilisateur (`get_queryset`)

Afin d'assurer la confidentialité des dépenses entre différents groupes d'utilisateurs, j'ai surchargé la méthode `get_queryset()` sur les ViewSets. Un utilisateur classique ne peut visualiser via l'API que les événements auxquels il participe et les dépenses qui y sont rattachées (les administrateurs `is_staff` conservant un accès global) :

```python
class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.prefetch_related("participants", "expenses").all()
    serializer_class = EventSerializer
    permission_classes = [IsEventParticipant]

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset
        return self.queryset.filter(participants=self.request.user).distinct()


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.select_related("payer", "event").all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsPayerOrEventParticipant]

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset
        return self.queryset.filter(
            Q(payer=self.request.user) | Q(event__participants=self.request.user)
        ).distinct()
```

---

## 4. Problématiques Techniques Résolues

### 1. Robustesse des validations sur requêtes partielles (`PATCH`)
- **Problème** : Lors d'une requête HTTP `PATCH /api/expenses/{id}/`, le client peut n'envoyer que le champ `amount`. Dans ce cas, `attrs.get('payer')` et `attrs.get('event')` renvoyaient `None`, ce qui faussait la validation croisée `validate()`.
- **Solution** : J'ai mis en place un mécanisme de repli intelligent avec `getattr(self.instance, 'payer', None)` et `getattr(self.instance, 'event', None)` permettant de combiner les données entrantes avec l'état existant en base.

### 2. Standardisation du Routage REST
- J'ai utilisé le `DefaultRouter` de DRF dans [`djancount/expenses/urls.py`](../djancount/expenses/urls.py) afin de générer automatiquement une arborescence REST uniforme (`/api/events/`, `/api/expenses/`) conforme aux conventions OpenAPI/Swagger.
