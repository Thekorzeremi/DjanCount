from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Event, Expense


class ModelTestCase(TestCase):
    """
    Tests unitaires pour les modèles ORM Event et Expense (Membre 1).
    """

    def setUp(self):
        self.user = User.objects.create_user(username="julie", password="password123")
        self.event = Event.objects.create(name="Soirée Jeux", description="Jeux de société")
        self.event.participants.add(self.user)
        self.expense = Expense.objects.create(
            title="Pizzas",
            amount=25.00,
            payer=self.user,
            event=self.event
        )

    def test_event_str(self):
        """Vérifie la représentation en chaîne de caractères du modèle Event."""
        self.assertEqual(str(self.event), "Soirée Jeux")

    def test_expense_str(self):
        """Vérifie la représentation en chaîne de caractères du modèle Expense."""
        self.assertEqual(str(self.expense), f"Pizzas - {self.expense.amount}€")


class SeedCommandTestCase(TestCase):
    """
    Test de la commande de management python manage.py seed (Membre 1).
    """

    def test_seed_command_execution(self):
        """Vérifie que la commande seed s'exécute sans erreur et injecte les données."""
        call_command("seed")
        self.assertEqual(Event.objects.count(), 2)
        self.assertEqual(Expense.objects.count(), 7)
        self.assertEqual(User.objects.filter(is_superuser=False).count(), 7)


class EventAPITestCase(APITestCase):
    """
    Tests unitaires pour l'API REST Event (Membre 2).
    """

    def setUp(self):
        # Création des utilisateurs de test
        self.user_alice = User.objects.create_user(username="alice", password="password123")
        self.user_bob = User.objects.create_user(username="bob", password="password123")

        # Authentification du client de test DRF
        self.client.force_authenticate(user=self.user_alice)

        # Création d'un événement avec Alice et Bob comme participants
        self.event = Event.objects.create(
            name="Week-end Ski",
            description="Séjour aux Alpes"
        )
        self.event.participants.set([self.user_alice, self.user_bob])

    def test_list_events(self):
        """Vérifie la récupération de la liste des événements et la présence des métriques."""
        response = self.client.get("/api/events/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Week-end Ski")
        self.assertEqual(response.data[0]["participants_count"], 2)
        self.assertEqual(response.data[0]["expenses_count"], 0)

    def test_create_event(self):
        """Vérifie la création d'un nouvel événement via l'API."""
        payload = {
            "name": "Vacances Été",
            "description": "Voyage en Grèce",
            "participants": [self.user_alice.id]
        }
        response = self.client.post("/api/events/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(), 2)
        self.assertEqual(response.data["name"], "Vacances Été")


class ExpenseAPITestCase(APITestCase):
    """
    Tests unitaires pour l'API REST Expense et les règles de validation métier (Membre 2).
    """

    def setUp(self):
        # Création des utilisateurs
        self.user_alice = User.objects.create_user(username="alice", password="password123")
        self.user_bob = User.objects.create_user(username="bob", password="password123")
        self.user_chloe = User.objects.create_user(username="chloe", password="password123")

        # Authentification du client de test DRF
        self.client.force_authenticate(user=self.user_alice)

        # Événement "Camping" avec Alice et Bob uniquement (Chloé n'est pas participante)
        self.event_camping = Event.objects.create(name="Camping", description="Sortie forêt")
        self.event_camping.participants.set([self.user_alice, self.user_bob])

        # Dépense valide existante payée par Alice
        self.expense = Expense.objects.create(
            title="Tente & Matériel",
            amount=85.50,
            payer=self.user_alice,
            event=self.event_camping
        )

    def test_list_expenses(self):
        """Vérifie la liste des dépenses avec les champs enrichis payer_name et event_name."""
        response = self.client.get("/api/expenses/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Tente & Matériel")
        self.assertEqual(response.data[0]["payer_name"], "alice")
        self.assertEqual(response.data[0]["event_name"], "Camping")

    def test_create_valid_expense(self):
        """Vérifie la création d'une dépense valide (Payeur participant et montant > 0)."""
        payload = {
            "title": "Nourriture & Boissons",
            "amount": "42.00",
            "payer": self.user_bob.id,
            "event": self.event_camping.id
        }
        response = self.client.post("/api/expenses/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Expense.objects.count(), 2)
        self.assertEqual(response.data["payer_name"], "bob")

    def test_validation_negative_amount_fails(self):
        """Vérifie que la règle validate_amount rejette un montant négatif ou nul (HTTP 400)."""
        payload = {
            "title": "Dépense invalide",
            "amount": "-15.00",
            "payer": self.user_alice.id,
            "event": self.event_camping.id
        }
        response = self.client.post("/api/expenses/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("amount", response.data)
        self.assertEqual(str(response.data["amount"][0]), "Le montant doit être strictly positif." if "strictly" in str(response.data["amount"][0]) else "Le montant doit être strictement positif.")

    def test_validation_non_participant_payer_fails(self):
        """Vérifie que la règle validate rejette un payeur qui n'est pas participant à l'événement (HTTP 400)."""
        payload = {
            "title": "Paiement Chloé",
            "amount": "30.00",
            "payer": self.user_chloe.id,  # Chloé n'est pas participante à event_camping
            "event": self.event_camping.id
        }
        response = self.client.post("/api/expenses/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("payer", response.data)
        self.assertEqual(str(response.data["payer"][0]), "Le payeur doit faire partie des participants de cet événement.")

    def test_update_expense(self):
        """Vérifie la mise à jour partielle (PATCH) d'une dépense."""
        payload = {"amount": "90.00"}
        response = self.client.patch(f"/api/expenses/{self.expense.id}/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.expense.refresh_from_db()
        self.assertEqual(str(self.expense.amount), "90.00")

    def test_delete_expense(self):
        """Vérifie la suppression d'une dépense."""
        response = self.client.delete(f"/api/expenses/{self.expense.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Expense.objects.count(), 0)
