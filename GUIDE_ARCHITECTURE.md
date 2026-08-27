# 📘 Guide d'Architecture & Dictionnaire des Fichiers - DjanCount

Ce document recense l'arborescence complète du projet **DjanCount**, le dictionnaire de rôle de chaque fichier, les **choix techniques fondamentaux**, ainsi qu'une **analyse rigoureuse de conformité par rapport au cours J3 (TP3 / DRF) et au Cahier des Charges**.

---

## 📌 1. Contexte du Projet

* **Nom du projet** : DjanCount (Application Web & API REST de gestion de dépenses partagées, type Tricount).
* **Technologies** : Python 3.10+, Django 5.2+, Django REST Framework (DRF), SimpleJWT, HTML5/CSS (Templates Django).
* **Équipe (4 Membres)** :
  - **Membre 1 (Julie)** : Core Django, Modèles, Admin & Script `seed.py`.
  - **Membre 2 (Seer)** : API REST DRF, Sérialiseurs (`serializers.py`), Validations Métier & ViewSets.
  - **Membre 3 (Conambot)** : Authentification JWT, Sécurité & Permissions DRF.
  - **Membre 4 (Rémi)** : Vue HTML classique, Algorithme du Bilan Financier & Template HTML.

---

## 📂 2. Arborescence Exhaustive du Projet

```text
DjanCount/
├── .gitignore                           # 🙈 Exclusion des fichiers temporaires (venv, db.sqlite3, __pycache__)
├── README.md                            # 📖 Guide d'installation et de lancement multi-plateforme
├── ORGANISATION.md                      # 🚀 Planning de la journée, répartition des tâches & workflow Git
├── GUIDE_ARCHITECTURE.md                # 📘 Présent guide d'architecture, dictionnaire & audit J3
├── requirements.txt                     # 📋 Dépendances du projet (Django, DRF, SimpleJWT, etc.)
│
├── docs/                                # 📄 Rapports individuels de contribution (Support de notation TD)
│   ├── RAPPORT_REMI.md                  # Rapport individuel de Rémi (Membre 4)
│   └── RAPPORT_SEER.md                  # Rapport individuel de Seer (Membre 2)
│
├── http-requests/                       # 🧪 Requêtes de test HTTP client (VS Code REST Client / Postman)
│   ├── events.http                      # Tests des endpoints API /api/events/
│   └── expenses.http                    # Tests des endpoints API /api/expenses/ (cas passants et erreurs 400)
│
└── djancount/                           # 🗂️ Dossier racine du projet Django (contenant manage.py)
    ├── manage.py                        # 🛠️ Script CLI Django (runserver, migrate, seed, etc.)
    ├── db.sqlite3                       # 🗄️ Base de données SQLite locale
    │
    ├── config/                          # ⚙️ Module de configuration globale de l'application
    │   ├── __init__.py                  # Package Python
    │   ├── settings.py                  # Configuration globale (INSTALLED_APPS, DATABASES, DRF, JWT)
    │   ├── urls.py                      # Routage d'URL principal (/admin/, /api/, tokens JWT)
    │   ├── asgi.py                      # Point d'entrée serveur web asynchrone (ASGI)
    │   └── wsgi.py                      # Point d'entrée serveur web classique (WSGI)
    │
    └── expenses/                        # 📦 Application métier "expenses"
        ├── __init__.py                  # Package Python
        ├── admin.py                     # Configuration de l'administration Django (/admin)
        ├── apps.py                      # Déclaration de l'application ExpensesConfig
        ├── models.py                    # Modèles ORM Event (Événement) et Expense (Dépense)
        ├── serializers.py               # Sérialiseurs DRF, métriques calculées et validations métier
        ├── views.py                     # ViewSets API REST (Membre 2) & Vue HTML Bilan (Membre 4)
        ├── permissions.py               # Permissions personnalisées de sécurité DRF (Membre 3)
        ├── urls.py                      # Routage API via DefaultRouter (/api/events/, /api/expenses/)
        ├── tests.py                     # Tests unitaires et d'intégration APITestCase DRF
        ├── README.md                    # Documentation interne de l'application expenses
        │
        ├── migrations/                  # 🧬 Fichiers de migration du schéma de base de données
        │   ├── __init__.py
        │   └── 0001_initial.py          # Migration initiale (création des tables Event et Expense)
        │
        └── management/                  # 🛠️ Commandes de management Django personnalisées
            ├── __init__.py
            └── commands/
                ├── __init__.py
                └── seed.py              # Script d'injection idempotente de données de démonstration
```

---

## 📄 3. Dictionnaire Détaillé des Fichiers & Leurs Rôles

### A. Racines & Documentation (`DjanCount/`)

* **`.gitignore`** : Définit les règles d'exclusion Git pour éviter de versionner les artefacts locaux (`venv/`, `db.sqlite3`, `.pyc`, `.DS_Store`).
* **`requirements.txt`** : Liste les packages Python obligatoires : `Django`, `djangorestframework`, `djangorestframework-simplejwt`, `django-debug-toolbar`.
* **`README.md`** : Guide complet d'installation et de lancement pour tout nouvel arrivant (création venv, pip install, migrations, seed, runserver).
* **`ORGANISATION.md`** : Document de cadrage d'équipe récapitulant les rôles de chacun (Membres 1 à 4), le planning de la journée et les consignes de git branch.
* **`GUIDE_ARCHITECTURE.md`** : Référentiel technique central (arborescence, choix de conception et conformité J3).

### B. Tests & Client HTTP (`http-requests/` et `docs/`)

* **`http-requests/events.http`** & **`expenses.http`** : Fichiers de test des requêtes REST pour exécuter facilement des appels `GET`, `POST`, `PUT`, `PATCH`, `DELETE` directement depuis l'IDE.
* **`docs/RAPPORT_*.md`** : Rapports individuels requis pour l'évaluation de TD.

### C. Configuration Centrale (`djancount/config/`)

* **`manage.py`** : Entrée principale en ligne de commande pour piloter Django (`migrate`, `seed`, `runserver`, `test`).
* **`config/settings.py`** : Fichier central de configuration. Contient la déclaration de `INSTALLED_APPS` (incluant `'rest_framework'` et `'expenses'`), la configuration du moteur SQLite, et les paramètres DRF/JWT.
* **`config/urls.py`** : Table de routage maître qui relie `/admin/` à l'interface d'admin, `/api/token/` pour SimpleJWT, et délègue le reste à `expenses.urls`.

### D. Application Métier (`djancount/expenses/`)

* **`expenses/models.py`** (Membre 1) : Définition des modèles ORM Django :
  - `Event` : Un événement avec un nom, une description et des participants (`ManyToManyField` vers `User`).
  - `Expense` : Une dépense liée à un `Event` (FK), un payeur `User` (FK), un titre, un montant (`DecimalField`) et une date.
* **`expenses/admin.py`** (Membre 1) : Configuration d'affichage sur `/admin/` (`list_display`, `list_filter`, `search_fields`, `filter_horizontal`).
* **`expenses/management/commands/seed.py`** (Membre 1) : Script d'alimentation de la base de données. Réinitialise et remplit la base avec des utilisateurs de test, des événements et des dépenses.
* **`expenses/serializers.py`** (Membre 2) :
  - `EventSerializer` : Sérialise les événements et inclut des métriques calculées `participants_count` et `expenses_count`.
  - `ExpenseSerializer` : Sérialise les dépenses avec validation métier `validate_amount` (`amount > 0`) et `validate` (vérification que le payeur est bien participant).
* **`expenses/views.py`** (Membres 2 & 4) :
  - `EventViewSet` & `ExpenseViewSet` : Controller DRF gérant les opérations CRUD avec optimisations ORM (`select_related`, `prefetch_related`).
  - Vue HTML `event_detail_view` (Membre 4) : Vue affichant le bilan financier.
* **`expenses/permissions.py`** (Membre 3) : Classes de permissions sécurisant l'API REST (`IsAuthenticatedOrReadOnly`).
* **`expenses/urls.py`** (Membres 2 & 4) : Déclare le `DefaultRouter` pour l'API REST (`/api/events/`, `/api/expenses/`) et la route web.
* **`expenses/tests.py`** : Suite de tests automatisés validant le bon fonctionnement des sérialiseurs et des ViewSets.

---

## 💡 4. Choix Techniques & Justifications (Support de Soutenance)

### 1. ORM et Relations de Données (Membre 1)
* **Choix** : Utilisation d'une relation `ManyToManyField` entre `Event` et `User` et d'une `ForeignKey` entre `Expense` et `Event`/`User`.
* **Raison** : Reflète exactement le besoin métier d'une application type Tricount : un événement regroupe plusieurs membres, et chaque dépense est payée par un membre pour un événement donné.
* **Idempotence de `seed.py`** : Le script efface les enregistrements existants avant d'injecter la donnée pour permettre d'exécuter `python manage.py seed` à n'importe quel moment sans générer de doublons.

### 2. Django REST Framework & Validations Métier (Membre 2)
* **`ModelSerializer` vs `Serializer`** : Utiliser `ModelSerializer` évite la duplication de code et génère automatiquement la persistance.
* **Séparation Lecture/Écriture** : Utilisation des champs d'IDs pour la création/modification, et ajout de champs calculés en lecture seule (`payer_name`, `event_name`) pour fournir au frontend des données complètes sans requêtes supplémentaires.
* **Optimisation contre le problème N+1 SQL** :
  - `select_related("payer", "event")` réalise une jointure SQL `JOIN` pour limiter les requêtes lors de la liste des dépenses.
  - `prefetch_related("participants", "expenses")` effectue une requête groupée pour charger les relations ManyToMany et les clés inverses sans surcharger la base.
* **Niveaux de Validation** :
  - Validation champ par champ (`validate_amount`) pour vérifier la stricte positivité du montant.
  - Validation globale multi-champs (`validate`) pour vérifier la cohérence métier (le payeur doit appartenir aux participants de l'événement).

### 3. Authentification & Permissions (Membre 3)
* **JSON Web Tokens (JWT)** : Authentification *stateless* adaptée aux API REST.
* **Permissions granulaires** : `IsAuthenticatedOrReadOnly` permet la consultation publique tout en protégeant les opérations d'écriture (POST, PUT, DELETE).

### 4. Algorithme du Bilan Financier (Membre 4)
* **Algorithme de calcul dans la vue HTML** :
  $$\text{Part théorique} = \frac{\text{Total des dépenses}}{\text{Nombre de participants}}$$
  $$\text{Solde net} = \text{Montant payé par l'utilisateur} - \text{Part théorique}$$
* **Affichage récapitulatif** : Permet de déterminer instantanément qui doit de l'argent et qui doit être remboursé.

---

## 🔍 5. Audit de Conformité avec le Cours J3 / TP3 & Cahier des Charges

| Exigence du Cahier des Charges (J3) | Fichier / Implémentation | Statut | Commentaire / Conformité |
| :--- | :--- | :---: | :--- |
| **1. Au moins 2 modèles Django liés (FK)** | [expenses/models.py](file:///c:/Users/seerm/OneDrive/Desktop/IPSSI/DJANgo/Projet/DjanCount/djancount/expenses/models.py) | ✅ **Conforme** | Modèles `Event` et `Expense` correctement modélisés avec `ForeignKey` et `ManyToManyField`. |
| **2. Admin Django fonctionnel sur les 2 modèles** | [expenses/admin.py](file:///c:/Users/seerm/OneDrive/Desktop/IPSSI/DJANgo/Projet/DjanCount/djancount/expenses/admin.py) | ✅ **Conforme** | Modèles enregistrés avec filtres, recherche et widgets d'affichage optimisés. |
| **3. API REST (ModelViewSet + DefaultRouter)** | [expenses/views.py](file:///c:/Users/seerm/OneDrive/Desktop/IPSSI/DJANgo/Projet/DjanCount/djancount/expenses/views.py), [expenses/urls.py](file:///c:/Users/seerm/OneDrive/Desktop/IPSSI/DJANgo/Projet/DjanCount/djancount/expenses/urls.py) | ✅ **Conforme** | `EventViewSet` et `ExpenseViewSet` intégrés via `DefaultRouter` sous `/api/`. |
| **4. Sérialiseur avec Validation Métier** | [expenses/serializers.py](file:///c:/Users/seerm/OneDrive/Desktop/IPSSI/DJANgo/Projet/DjanCount/djancount/expenses/serializers.py) | ✅ **Conforme** | Validation de montant (`validate_amount`) et validation croisée payeur/participant (`validate`). |
| **5. Declaration des Apps DRF & Paramètres** | [config/settings.py](file:///c:/Users/seerm/OneDrive/Desktop/IPSSI/DJANgo/Projet/DjanCount/djancount/config/settings.py) | ✅ **Conforme** | `'rest_framework'` ajouté dans `INSTALLED_APPS`. |
| **6. Authentification JWT & Permissions** | [config/settings.py](file:///c:/Users/seerm/OneDrive/Desktop/IPSSI/DJANgo/Projet/DjanCount/djancount/config/settings.py), `requirements.txt` | 🔄 **En cours** | Package `djangorestframework-simplejwt` référencé. Endpoints JWT à finaliser par Membre 3. |
| **7. Vue HTML & Template (Bilan)** | `expenses/views.py`, `templates/` | 🔄 **En cours** | Implémentation du bilan financier en cours par Membre 4. |
| **8. Documentation & Instructions (README)** | [README.md](file:///c:/Users/seerm/OneDrive/Desktop/IPSSI/DJANgo/Projet/DjanCount/README.md) | ✅ **Conforme** | Instructions pas à pas prêtes pour l'exécution du projet. |
| **9. Rapport individuel de contribution** | `docs/` | ✅ **Conforme** | Rapports individuels disponibles dans le dossier `docs/`. |

---

## 🚀 6. Guide de Mise en Route Rapide (Windows PowerShell)

```powershell
# 1. Se placer dans le dossier du projet Django
cd djancount

# 2. Vérifier que l'environnement virtuel est actif et appliquer les migrations
..\venv\Scripts\python.exe manage.py migrate

# 3. Charger les données de démonstration réexécutables
..\venv\Scripts\python.exe manage.py seed

# 4. Exécuter les vérifications et les tests
..\venv\Scripts\python.exe manage.py check
..\venv\Scripts\python.exe manage.py test

# 5. Démarrer le serveur de développement
..\venv\Scripts\python.exe manage.py runserver
```
