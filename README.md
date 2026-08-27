# 🚀 DjanCount — Application & API REST de Gestion de Dépenses Partagées

**DjanCount** est une application web et une API REST inspirée de *Tricount*, développée avec **Django 5.2** et **Django REST Framework (DRF)**.  
Elle permet de créer des événements entre amis, d'y enregistrer des dépenses et de calculer automatiquement le bilan financier (qui doit quoi à qui).

---

## 🛠️ Stack Technique & Prérequis

* **Python** : `3.10` ou supérieur
* **Framework Web** : `Django 5.2+`
* **API REST** : `Django REST Framework 3.16+`
* **Sécurité & Auth** : `djangorestframework-simplejwt`
* **CORS** : `django-cors-headers`
* **Base de données** : SQLite (par défaut)

---

## 🗂️ Modèles de Données & Architecture ORM

L'application repose sur deux modèles principaux reliés au modèle `User` natif de Django (`django.contrib.auth.models.User`) :

### 1. Modèle `Event` (Événement)
Représente un groupe de dépenses pour une occasion donnée (ex: *"Week-end à la mer"*).
* `name` (`CharField`) : Nom de l'événement.
* `description` (`TextField`) : Description optionnelle de l'événement.
* `participants` (`ManyToManyField` $\rightarrow$ `User`) : Liste des utilisateurs participant à l'événement.

### 2. Modèle `Expense` (Dépense)
Représente un paiement effectué par un membre du groupe pour l'événement.
* `title` (`CharField`) : Intitulé de la dépense (ex: *"Essence"*, *"Courses"*).
* `amount` (`DecimalField`) : Montant payé en Euros (doit être $> 0$).
* `payer` (`ForeignKey` $\rightarrow$ `User`) : Membre ayant réglé la dépense.
* `event` (`ForeignKey` $\rightarrow$ `Event`) : Événement auquel est rattachée la dépense.
* `date` (`DateField`) : Date d'enregistrement automatique (`auto_now_add`).

### 💡 Validations Métiers Clés
1. **Montant Positif (`validate_amount`)** : Une dépense doit impérativement avoir un montant strictement supérieur à zéro.
2. **Payeur Participant (`validate`)** : Le payeur (`payer`) d'une dépense doit obligatoirement figurer dans la liste des `participants` de l'événement concerné.

---

## 💻 Guide d'Installation & Lancement Multi-plateformes

### Étape 1 : Cloner le projet et ouvrir un terminal
```bash
git clone <url-du-depot>
cd DjanCount
```

---

### Étape 2 : Créer l'environnement virtuel (`venv`)

* **macOS / Linux** :
  ```bash
  python3 -m venv venv
  ```
* **Windows (PowerShell ou CMD)** :
  ```powershell
  python -m venv venv
  ```

---

### Étape 3 : Activer l'environnement virtuel

* **macOS / Linux (Bash / Zsh)** :
  ```bash
  source venv/bin/activate
  ```
* **Windows (PowerShell)** :
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
  *(Si PowerShell bloque l'exécution des scripts : lancez `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process`)*
* **Windows (CMD / Invite de commandes)** :
  ```cmd
  .\venv\Scripts\activate.bat
  ```

---

### Étape 4 : Installer les dépendances

```bash
pip install -r requirements.txt
```

---

### Étape 5 : Préparer la base de données et les migrations

Se placer dans le répertoire du projet Django `djancount/` :

```bash
cd djancount
python manage.py migrate
```

---

### Étape 6 : Créer un compte Administrateur (Superuser)

Pour accéder à l'interface d'administration Django (`/admin/`), créez votre compte administrateur en ligne de commande :

```bash
python manage.py createsuperuser
```

Saisissez les informations demandées par le terminal :
- **Username** (ex: `admin`)
- **Email address** (ex: `admin@example.com`)
- **Password** (saisissez votre mot de passe, puis confirmez-le)

---

### Étape 7 : Injecter les données de démonstration (Seed)

Une commande personnalisée permet de remplir la base de données avec des utilisateurs, événements et dépenses de démonstration :

```bash
python manage.py seed
```

> **Comptes de test injectés par le seed** (mot de passe : `password123` pour tous) :  
> `alice`, `bob`, `chloe`, `seer`, `julie`, `conambot`, `remi`.

---

### Étape 8 : Exécuter la suite de tests unitaires

Pour valider le bon fonctionnement de l'application et de l'API REST :

```bash
python manage.py test
```

---

### Étape 9 : Démarrer le serveur de développement

```bash
python manage.py runserver
```

L'application est désormais accessible sur `http://127.0.0.1:8000/`.

---

## 🔑 Accès au Panneau d'Administration Django (`/admin/`)

1. Démarrez le serveur de développement avec `python manage.py runserver`.
2. Ouvrez votre navigateur web et rendez-vous sur : **`http://127.0.0.1:8000/admin/`**
3. Connectez-vous avec l'identifiant et le mot de passe créés à l'Étape 6 (`python manage.py createsuperuser`).
4. Depuis le panneau d'administration, vous pouvez gérer et visualiser les **Utilisateurs**, les **Événements** (`Event`) et les **Dépenses** (`Expense`).

---

## 🌐 Endpoints & Accès à l'Application

| Ressource | URL | Méthodes | Description |
| :--- | :--- | :---: | :--- |
| **Panneau Admin Django** | `http://127.0.0.1:8000/admin/` | `GET`, `POST` | Interface d'administration globale |
| **API Événements** | `http://127.0.0.1:8000/api/events/` | `GET`, `POST`, `PUT`, `PATCH`, `DELETE` | CRUD des événements |
| **API Dépenses** | `http://127.0.0.1:8000/api/expenses/` | `GET`, `POST`, `PUT`, `PATCH`, `DELETE` | CRUD des dépenses |
| **Auth JWT Obtenir Token** | `http://127.0.0.1:8000/api/token/` | `POST` | Obtention des jetons `access` et `refresh` |
| **Auth JWT Rafraîchir Token** | `http://127.0.0.1:8000/api/token/refresh/` | `POST` | Renouvellement du jeton `access` |

---

## 🧪 Requêtes de Test HTTP Client

Des fichiers de test prêts à l'emploi sont disponibles dans le dossier `http-requests/` pour tester les endpoints directement depuis l'éditeur (extension REST Client sous VS Code) :
- `http-requests/events.http` : Tests des endpoints API /api/events/
- `http-requests/expenses.http` : Tests des endpoints API /api/expenses/ (cas passants et erreurs 400)

---

## 📁 Architecture du Projet

Pour comprendre en détail la structure des fichiers, les rôles des membres de l'équipe et l'audit de conformité, consultez le [GUIDE_ARCHITECTURE.md](GUIDE_ARCHITECTURE.md).