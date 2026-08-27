from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from expenses.models import Event, Expense


class Command(BaseCommand):
    help = "Injecte des données de démonstration"

    def handle(self, *args, **kwargs):
        Expense.objects.all().delete()
        Event.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()

        alice = User.objects.create_user("alice", password="password123")
        bob = User.objects.create_user("bob", password="password123")
        chloe = User.objects.create_user("chloe", password="password123")

        event1 = Event.objects.create(
            name="Week-end à la mer",
            description="Trois jours à Biarritz",
        )
        event1.participants.set([alice, bob, chloe])

        Expense.objects.create(title="Essence", amount=45.50, payer=alice, event=event1)
        Expense.objects.create(title="Courses", amount=78.20, payer=bob, event=event1)
        Expense.objects.create(title="Restaurant", amount=120.00, payer=chloe, event=event1)

        self.stdout.write(self.style.SUCCESS("Seed terminé."))