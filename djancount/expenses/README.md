# 👨‍💻 Membre 1 : Core Django, Modèles, Admin & Fixtures

Cette partie du projet DjanCount couvre la modélisation des données, leur gestion dans l'admin Django, et l'injection de données de démonstration.

## 📁 Structure

```
djancount/
├── manage.py
├── config/              # configuration globale du projet
│   ├── settings.py
│   ├── urls.py
│   └── ...
└── expenses/            # app métier
    ├── models.py        # modèles Event et Expense
    ├── admin.py          # enregistrement dans l'interface admin
    ├── migrations/
    └── management/
        └── commands/
            └── seed.py   # script d'injection de données de test
```

## 🗂️ Modèles

### `Event`

| Champ          | Type              | Description                            |
| -------------- | ----------------- | -------------------------------------- |
| `name`         | `CharField`       | Nom de l'événement                     |
| `description`  | `TextField`       | Description libre                      |
| `participants` | `ManyToManyField` | Utilisateurs participant à l'événement |

### `Expense`

| Champ    | Type                | Description                             |
| -------- | ------------------- | --------------------------------------- |
| `title`  | `CharField`         | Intitulé de la dépense                  |
| `amount` | `DecimalField`      | Montant payé                            |
| `payer`  | `ForeignKey(User)`  | Utilisateur ayant payé                  |
| `event`  | `ForeignKey(Event)` | Événement concerné                      |
| `date`   | `DateField`         | Date de création (auto, non modifiable) |

**Relations :**

- `Event ↔ User` : plusieurs-à-plusieurs (`ManyToManyField`), un événement a plusieurs participants et un utilisateur peut appartenir à plusieurs événements.
- `Expense → User` et `Expense → Event` : plusieurs-vers-un (`ForeignKey`), chaque dépense a un seul payeur et appartient à un seul événement.
- `on_delete=models.CASCADE` : si un `User` ou un `Event` est supprimé, ses dépenses liées le sont aussi.

## ⚙️ Admin

`Event` et `Expense` sont enregistrés dans `expenses/admin.py` avec :

- `list_display` pour afficher les colonnes utiles dans la liste
- `list_filter` sur `event` et `payer` pour filtrer les dépenses
- `search_fields` pour la recherche par titre/nom
- `filter_horizontal` sur `participants` pour un widget de sélection multiple lisible

Accessible sur `/admin/` après création d'un superutilisateur.

## 🌱 Données de démonstration

Une commande de management custom injecte des données de test :

```bash
python manage.py seed
```

Elle crée 3 utilisateurs, 1 événement, et plusieurs dépenses associées. La commande vide d'abord les tables concernées pour rester idempotente (relançable sans doublons).

## 🚀 Mise en route

```bash
cd djancount

# Appliquer le schéma en base
python manage.py makemigrations expenses
python manage.py migrate

# Créer un compte admin
python manage.py createsuperuser

# Injecter des données de démo
python manage.py seed

# Lancer le serveur
python manage.py runserver
```

Puis se connecter sur `http://127.0.0.1:8000/admin/` pour vérifier que `Event` et `Expense` apparaissent avec les données injectées.
