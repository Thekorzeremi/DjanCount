# Rapport Individuel de Contribution - Projet DjanCount

**Nom & Prénom :** KORZENIOWSKI Rémi
**Date :** 27/08/2026
**Module attribué :** Vue HTML, Template & Algorithme du Bilan Financier

---

### 1. Description du travail réalisé
En tant que Membre 4, j'ai développé la partie "Vue HTML" du projet DjanCount. Mes missions consistaient à :

- Écrire la vue classique Django `event_detail_view` dans `expenses/views.py`
- Développer l'algorithme Python du **Bilan Financier** permettant de calculer les dettes entre participants
- Créer le template HTML `expenses/templates/expenses/event_detail.html` affichant le résumé, le détail des dépenses, les soldes et les transactions à effectuer
- Configurer la route URL correspondante dans `expenses/urls.py`

Fichiers développés : `expenses/views.py` (partie Membre 4), `expenses/templates/expenses/event_detail.html`, `expenses/urls.py` (ajout de la route HTML).

### 2. Implémentation technique et extraits de code (Snippets)

**La vue Django (`event_detail_view`)** utilise une fonction classique prenant `request` et `event_id` comme paramètres. J'utilise `get_object_or_404` pour récupérer l'événement depuis la base de données, puis je récupère les participants et dépenses via les relations ORM :

```python
def event_detail_view(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    participants = list(event.participants.all())
    expenses = event.expenses.select_related("payer").all()
```

**L'algorithme du bilan financier** fonctionne en 3 étapes :
1. Calcul du total des dépenses et de la part théorique par personne (`Total / nb_participants`)
2. Calcul du solde net de chaque participant (ce qu'il a payé moins sa part théorique)
3. Simplification des transactions via un algorithme glouton à deux pointeurs : on identifie les débiteurs (solde négatif) et les créanciers (solde positif), puis on minimise le nombre de virements en appariant montants :

```python
while i < len(debtors) and j < len(creditors):
    amount = min(debtors[i][1], creditors[j][1])
    transactions.append({
        'from': debtors[i][0],
        'to': creditors[j][0],
        'amount': round(amount, 2)
    })
    debtors[i][1] -= amount
    creditors[j][1] -= amount
```

**Le template HTML** affiche 4 sections : résumé (total + part par personne), détail des dépenses, soldes avec coloration verte/rouge selon le signe, et la liste des transactions à effectuer. J'ai utilisé du CSS inline pour un rendu propre sans dépendance externe.

### 3. Difficultés rencontrées et solutions
- **Difficulté initiale** : La vue utilisait des données mockées hardcodées (listes statiques) au lieu de requêter la base de données. La première version ne prenait pas le paramètre `event_id`, rendant la vue inaccessible. Solution : refonte complète de la fonction avec `get_object_or_404` et les relations ORM.
- **Gestion des objets User** : Les dépenses de la base de données retournent des objets `User` (ForeignKey) plutôt que des strings. Il a fallu adapter l'algorithme pour travailler avec `expense.payer.first_name` au lieu de simples chaînes de caractères.

### 4. Compréhension de l'application globale
Le projet DjanCount est une application de gestion de dépenses partagées type Tricount. Voici le rôle des 3 autres parties :

- **Julie (Membre 1)** a créé les modèles de données `Event` et `Expense` avec leurs relations (ForeignKey, ManyToManyField), configuré l'interface d'admin Django pour la gestion visuelle des données, et écrit un script `seed.py` pour injecter des données de test.
- **Seer (Membre 2)** a implémenté l'API REST avec Django REST Framework : les sérialiseurs `EventSerializer` et `ExpenseSerializer` avec validations métier (montant > 0, payeur participant à l'événement), ainsi que les ViewSets offrant le CRUD complet.
- **Conambot (Membre 3)** a configuré l'authentification JWT via `djangorestframework-simplejwt` avec les routes `/api/token/` et `/api/token/refresh/`, et créé les classes de permissions personnalisées `IsEventParticipant` et `IsPayerOrEventParticipant` pour sécuriser les accès.
