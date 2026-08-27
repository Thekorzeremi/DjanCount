from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    participants = models.ManyToManyField(User, related_name="events")

    def __str__(self):
        return self.name


class Expense(models.Model):
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="expenses_paid")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="expenses")
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.amount}€"

