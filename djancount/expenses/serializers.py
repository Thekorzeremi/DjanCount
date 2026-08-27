from rest_framework import serializers
from .models import Event, Expense


class EventSerializer(serializers.ModelSerializer):

    """
    Sérialiseur pour le modèle Event.
    Gère la conversion JSON des événements et inclut des champs calculés
    en lecture seule (nombre de participants, nombre de dépenses).
    """
    participants_count = serializers.IntegerField(source="participants.count", read_only=True)
    expenses_count = serializers.IntegerField(source="expenses.count", read_only=True)
    
    class Meta:
        model = Event
        fields = [
            "id", "name", "description", "participants", "participants_count", "expenses_count"
        ]
        read_only_fields = ["id"]


class ExpenseSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le modèle Expense.
    Expose les données des dépenses et vérifie la validité des montants
    et la participation du payeur à l'événement.
    """
    payer_name = serializers.CharField(source="payer.username", read_only=True)
    event_name = serializers.CharField(source="event.name", read_only=True)
    
    class Meta:
        model = Expense
        fields = ["id", "title", "amount", "payer", "payer_name", "event", "event_name", "date"]
        read_only_fields = ["id", "date"]

    def validate_amount(self, value):
        """
        Règle de validation métier :
        Vérifie que le montant de la dépense est strictement positif (> 0).
        """
        if value <= 0:
            raise serializers.ValidationError("Le montant doit être strictement positif.")
        return value

    def validate(self, attrs):
        """
        Règle de validation métier globale :
        Vérifie que le payeur fait bien partie de la liste des participants de l'événement.
        Gère à la fois la création (POST) et la mise à jour partielle (PATCH).
        """
        payer = attrs.get('payer', getattr(self.instance, 'payer', None))
        event = attrs.get('event', getattr(self.instance, 'event', None))
        
        if event and payer and payer not in event.participants.all():
            raise serializers.ValidationError(
                {"payer": "Le payeur doit faire partie des participants de cet événement."}
            )
        return attrs


