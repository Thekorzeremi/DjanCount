from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from expenses.models import Event, Expense


class Command(BaseCommand):
    help = "Injecte des données de démonstration"

    def handle(self, *args, **kwargs):
        Expense.objects.all().delete()
        Event.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()

        alice = User.objects.create_user("alice", email="alice@example.com", password="password123", first_name="Alice")
        bob = User.objects.create_user("bob", email="bob@example.com", password="password123", first_name="Bob")
        chloe = User.objects.create_user("chloe", email="chloe@example.com", password="password123", first_name="Chloé")
        seer = User.objects.create_user("seer", email="seer@example.com", password="password123", first_name="Seer")
        julie = User.objects.create_user("julie", email="julie@example.com", password="password123", first_name="Julie")
        conambot = User.objects.create_user("conambot", email="conambot@example.com", password="password123", first_name="Conambot")
        remi = User.objects.create_user("remi", email="remi@example.com", password="password123", first_name="Rémi")

        event1 = Event.objects.create(
            name="Week-end à la mer",
            description="Trois jours à Biarritz",
        )
        event1.participants.set([alice, bob, chloe])

        Expense.objects.create(title="Essence", amount=45.50, payer=alice, event=event1)
        Expense.objects.create(title="Courses", amount=78.20, payer=bob, event=event1)
        Expense.objects.create(title="Restaurant", amount=120.00, payer=chloe, event=event1)

        event2 = Event.objects.create(
            name="Week-end Biarritz Équipe",
            description="Séjour au bord de la mer en équipe de dev",
        )
        event2.participants.set([seer, julie, conambot, remi])

        Expense.objects.create(title="Péage et Essence", amount=65.40, payer=seer, event=event2)
        Expense.objects.create(title="Courses Airbnb", amount=120.80, payer=julie, event=event2)
        Expense.objects.create(title="Location Planches de Surf", amount=80.00, payer=conambot, event=event2)
        Expense.objects.create(title="Dîner Fruits de mer", amount=145.00, payer=remi, event=event2)

        self.stdout.write(self.style.SUCCESS("Seed terminé : 7 utilisateurs de test (Alice, Bob, Chloé, Seer, Julie, Conambot, Rémi), 2 événements et 7 dépenses injectés."))

