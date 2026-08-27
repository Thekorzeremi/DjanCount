# 📊 DjanCount - Application Web & API REST de Gestion de Dépenses Partagées

**DjanCount** est une application web et API REST d'équilibrage de dépenses de groupe (type *Tricount*), développée avec **Python**, **Django**, **Django REST Framework (DRF)** et **SimpleJWT**.

L'application permet de créer des événements (ex: *"Week-end à la mer"*), d'y inscrire des participants, d'enregistrer des dépenses payées par différents membres, et d'obtenir automatiquement le bilan financier individuel ainsi que la liste minimale des virements à effectuer pour équilibrer les comptes.

---

## 🚀 1. Prérequis & Installation

### Prérequis
- **Python 3.10+**
- **Git**

### Étapes d'installation

1. **Cloner le répertoire ou se placer à la racine du projet** :
   ```bash
   cd DjanCount
   ```

2. **Créer et activer l'environnement virtuel** :
   - **Windows (PowerShell)** :
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```
   - **Linux / macOS** :
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

---

## 🗄️ 2. Base de données & Initialisation

Se placer dans le dossier `djancount` où se situe `manage.py` :
```bash
cd djancount
```

### 1. Appliquer les migrations
```bash
python manage.py migrate
```

### 2. Injecter les données de démonstration (Seed)
Un script de seed sur mesure permet de peupler la base avec **7 utilisateurs**, **2 événements** et **7 dépenses** de test :
```bash
python manage.py seed
```

### 3. Créer un Administrateur (Superuser)
```bash
python manage.py createsuperuser
```
*(Indiquez votre nom d'utilisateur, e-mail et mot de passe)*

---

## 🖥️ 3. Lancement du Serveur

Lancez le serveur de développement Django :
```bash
python manage.py runserver 8000
```
Le serveur sera accessible sur : `http://127.0.0.1:8000/`

---

## 🌐 4. Guide des URLs & Endpoints

### 🖼️ Interface Web HTML
- **Bilan Financier d'un Événement** : `GET http://127.0.0.1:8000/event/<event_id>/`
  - Exemple Événement 1 : [http://127.0.0.1:8000/event/1/](http://127.0.0.1:8000/event/1/)
  - Exemple Événement 2 : [http://127.0.0.1:8000/event/2/](http://127.0.0.1:8000/event/2/)
- **Interface Administrateur Django** : `GET http://127.0.0.1:8000/admin/`

---

### 🔑 Authentification API REST (SimpleJWT)

Pour effectuer des requêtes modificatrices (POST, PUT, DELETE) ou accéder aux événements réservés aux participants, vous devez obtenir un **Token JWT** :

1. **Obtenir le Token JWT** (`POST http://127.0.0.1:8000/api/token/`)
   - **Body JSON** :
     ```json
     {
       "username": "alice",
       "password": "password123"
     }
     ```
   - **Réponse (200 OK)** :
     ```json
     {
       "refresh": "<refresh_token>",
       "access": "<access_token>"
     }
     ```

2. **Utiliser le Token** :  
   Ajoutez le header HTTP suivant à vos requêtes API :
   ```http
   Authorization: Bearer <access_token>
   ```

3. **Rafraîchir le Token** (`POST http://127.0.0.1:8000/api/token/refresh/`)
   - **Body JSON** : `{"refresh": "<refresh_token>"}`

---

### 📡 Endpoints API REST (DRF)

Tous les endpoints API sont enregistrés sous le préfixe `/api/` :

| Méthode | Route API | Description | Permission |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/events/` | Liste des événements du participant | Token JWT |
| `POST` | `/api/events/` | Créer un nouvel événement | Token JWT |
| `GET` | `/api/events/{id}/` | Détail d'un événement | Participant |
| `PUT / PATCH` | `/api/events/{id}/` | Modifier un événement | Participant |
| `DELETE` | `/api/events/{id}/` | Supprimer un événement | Participant |
| `GET` | `/api/expenses/` | Liste des dépenses associées | Token JWT |
| `POST` | `/api/expenses/` | Enregistrer une nouvelle dépense | Token JWT + Validator |
| `GET` | `/api/expenses/{id}/` | Détail d'une dépense | Payeur / Participant |
| `PUT / PATCH` | `/api/expenses/{id}/` | Modifier une dépense | Payeur / Participant |
| `DELETE` | `/api/expenses/{id}/` | Supprimer une dépense | Payeur / Participant |

---

## 🛡️ 5. Validations Métiers & Sécurité

1. **Validation du Montant (`validate_amount`)** :
   - Le montant d'une dépense doit être **strictement positif (> 0)**.
   - En cas de montant `<= 0`, l'API renvoie un code `400 Bad Request` :
     ```json
     {
       "amount": ["Le montant doit être strictement positif."]
     }
     ```

2. **Validation du Payeur (`validate`)** :
   - Le payeur d'une dépense doit impérativement faire partie de la liste des **participants de l'événement**.
   - En cas d'incohérence, l'API renvoie un code `400 Bad Request` :
     ```json
     {
       "payer": ["Le payeur doit faire partie des participants de cet événement."]
     }
     ```

---

## 👥 6. Organisation de l'Équipe & Architecture

| Membre | Domaine & Responsabilités | Fichiers Clés |
| :--- | :--- | :--- |
| **Julie** (Membre 1) | Modèles ORM, Admin Django & Fixtures Seed | [`djancount/expenses/models.py`](djancount/expenses/models.py), [`djancount/expenses/admin.py`](djancount/expenses/admin.py) |
| **Seer** (Membre 2) | API REST DRF, Sérialiseurs & Validations Métiers | [`djancount/expenses/serializers.py`](djancount/expenses/serializers.py), [`djancount/expenses/views.py`](djancount/expenses/views.py) |
| **Conambot** (Membre 3) | Authentification SimpleJWT & Permissions DRF | [`djancount/expenses/permissions.py`](djancount/expenses/permissions.py), [`http-requests/jwt.http`](http-requests/jwt.http) |
| **Rémi** (Membre 4) | Vue Web HTML, Template & Algorithme du Bilan | [`djancount/expenses/views.py`](djancount/expenses/views.py), [`djancount/expenses/templates/expenses/event_detail.html`](djancount/expenses/templates/expenses/event_detail.html) |

---

## 📄 7. Rapports de Contribution

Les rapports individuels de contribution pour la soutenance se trouvent dans le dossier [`docs/`](docs/) :
- [`docs/RAPPORT_SEER.md`](docs/RAPPORT_SEER.md)
- [`docs/RAPPORT_REMI.md`](docs/RAPPORT_REMI.md)
