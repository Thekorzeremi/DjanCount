# Rapport Individuel de Contribution - Projet DjanCount

**Nom & Prénom :** Julie
**Date :** 27/08/2026
**Module attribué :** Core Django, Modèles, Admin & Fixtures

---

### 1. Description du travail réalisé

En tant que Membre 1, j'ai posé les fondations du projet DjanCount : la modélisation des données, leur exposition dans l'interface d'administration Django, et l'injection de données de démonstration permettant aux autres membres de développer et tester leurs propres parties (API, permissions, vue HTML) sans attendre que la base soit peuplée manuellement.

Mes missions ont couvert :

- La conception et l'écriture des modèles `Event` et `Expense` dans `expenses/models.py`, avec leurs relations vers le modèle `User` natif de Django.
- La configuration de l'admin Django (`expenses/admin.py`) pour permettre une gestion visuelle et filtrable des deux modèles.
- L'écriture d'une commande de management `seed.py` pour générer automatiquement des utilisateurs, un événement et des dépenses de test.
- La mise en place et le débogage de l'environnement de développement (venv, version de Python, structure du projet Django) nécessaire au bon fonctionnement du reste de l'équipe.

Fichiers développés : `expenses/models.py`, `expenses/admin.py`, `expenses/management/commands/seed.py`.

### 2. Implémentation technique et extraits de code (Snippets)

**Le modèle `Event`** représente un événement partagé et sa relation avec les participants :

```python
class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    participants = models.ManyToManyField(User, related_name="events")

    def __str__(self):
        return self.name
```

J'ai choisi `ManyToManyField` pour `participants` car la relation est symétrique et multiple des deux côtés : un événement compte plusieurs participants, et un utilisateur peut appartenir à plusieurs événements simultanément. Le `related_name="events"` permet ensuite de remonter la relation depuis un `User` (`user.events.all()`) sans passer par le nom de modèle par défaut.

**Le modèle `Expense`** représente une dépense rattachée à un événement et payée par un utilisateur :

```python
class Expense(models.Model):
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="expenses_paid")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="expenses")
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.amount}€"
```

Contrairement à `participants`, `payer` et `event` sont des `ForeignKey` : chaque dépense a un seul payeur et appartient à un seul événement, la relation est donc plusieurs-vers-un. J'ai utilisé `on_delete=models.CASCADE` pour que la suppression d'un `User` ou d'un `Event` entraîne automatiquement celle des dépenses associées, évitant des enregistrements orphelins. Le champ `date` utilise `auto_now_add=True` plutôt que `auto_now` : la date est figée à la création et n'est plus modifiée lors des sauvegardes ultérieures, ce qui correspond mieux à la sémantique d'une date de dépense.

**La configuration de l'admin** rend les deux modèles gérables et lisibles depuis l'interface :

```python
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)
    filter_horizontal = ("participants",)


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("title", "amount", "payer", "event", "date")
    list_filter = ("event", "payer")
    search_fields = ("title",)
```

`filter_horizontal` remplace le sélecteur multiple par défaut, peu ergonomique pour une `ManyToManyField`, par un widget à deux colonnes bien plus lisible pour choisir les participants. `list_filter` sur `event` et `payer` permet de retrouver rapidement toutes les dépenses d'un événement ou d'un utilisateur donné directement depuis la liste.

**Le script de seed**, implémenté comme une management command (`python manage.py seed`), crée un jeu de données cohérent et idempotent (la commande vide les tables concernées avant de les repeupler, pour pouvoir être relancée sans créer de doublons) :

```python
class Command(BaseCommand):
    help = "Injecte des données de démonstration"

    def handle(self, *args, **kwargs):
        Expense.objects.all().delete()
        Event.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()

        alice = User.objects.create_user("alice", password="password123")
        bob = User.objects.create_user("bob", password="password123")
        chloe = User.objects.create_user("chloe", password="password123")

        event1 = Event.objects.create(name="Week-end à la mer", description="Trois jours à Biarritz")
        event1.participants.set([alice, bob, chloe])

        Expense.objects.create(title="Essence", amount=45.50, payer=alice, event=event1)
        Expense.objects.create(title="Courses", amount=78.20, payer=bob, event=event1)
        Expense.objects.create(title="Restaurant", amount=120.00, payer=chloe, event=event1)
```

Ce script a été indispensable pour que Seer (API), Conambot (permissions/JWT) et Rémi (vue HTML) disposent immédiatement de données réalistes pour tester leurs propres modules sans dépendre d'une saisie manuelle répétée via l'admin.
