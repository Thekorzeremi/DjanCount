# Explications Complètes du Projet DjanCount

> Application Web & API REST de gestion de dépenses partagées (type Tricount)
> Stack : Python 3.11, Django 5.2, Django REST Framework, SimpleJWT

---

## Table des matières

1. [Architecture globale](#1-architecture-globale)
2. [manage.py](#2-managepy)
3. [config/settings.py](#3-configsettingspy)
4. [config/urls.py](#4-configurlspy)
5. [config/wsgi.py & asgi.py](#5-configwsgipy--asgipy)
6. [expenses/apps.py](#6-expensesappspy)
7. [expenses/models.py](#7-expensesmodelspy)
8. [expenses/admin.py](#8-expensesadminpy)
9. [expenses/serializers.py](#9-expensesserializerspy)
10. [expenses/permissions.py](#10-expensespermissionspy)
11. [expenses/views.py](#11-expensesviewspy)
12. [expenses/urls.py](#12-expensesurlspy)
13. [expenses/migrations/0001_initial.py](#13-expensesmigrations0001_initialpy)
14. [expenses/management/commands/seed.py](#14-expensesmanagementcommandsseedpy)
15. [expenses/templates/expenses/event_detail.html](#15-expensestemplatesexpensesevent_detailhtml)
16. [expenses/templates/expenses/home.html](#16-expensestemplatesexpenseshomehtml)
17. [drf-spectacular (Swagger UI)](#17-drf-spectacular-swagger-ui)
18. [requirements.txt](#18-requirementstxt)
19. [Algorithme du bilan financier — Ligne par ligne](#19-algorithme-du-bilan-financier--ligne-par-ligne)

---

## 1. Architecture globale

```
Requête HTTP du client (navigateur ou Postman)
        │
        ▼
┌─────────────────────────────────────────────────────────┐
│                   config/urls.py                        │
│          Routage : quelle URL → quelle vue ?            │
└──────────┬──────────────────────┬───────────────────────┘
           │                      │
     Route /api/...         Route /event/{id}/
           │                      │
           ▼                      ▼
┌──────────────────┐    ┌─────────────────────────────┐
│  ViewSet DRF     │    │  Fonction classique Django  │
│  (API REST JSON) │    │  (rendu HTML via template)  │
└────────┬─────────┘    └──────────┬──────────────────┘
         │                         │
         ▼                         ▼
┌──────────────────┐    ┌─────────────────────────────┐
│  Serializer DRF  │    │  Algorithme bilan financier │
│  Validation +    │    │  Calcul des soldes +        |
│  conversion JSON │    │  transactions optimisées    │
└────────┬─────────┘    └──────────┬──────────────────┘
         │                         │
         ▼                         ▼
┌─────────────────────────────────────────────────────────┐
│                expenses/permissions.py                  │
│         Contrôle d'accès (qui peut voir quoi ?)         │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                  expenses/models.py                     │
│        ORM Django : Event et Expense                    │
│        Requêtes SQL générées automatiquement            │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│              Base de données SQLite (db.sqlite3)        │
│              Stockage persistant des données            │
└─────────────────────────────────────────────────────────┘
```

### Structure des fichiers

```
DjanCount/
├── djancount/                    # Racine Django
│   ├── manage.py                 # Point d'entrée CLI
│   ├── db.sqlite3                # Base SQLite (générée)
│   ├── config/                   # Configuration globale
│   │   ├── __init__.py           # Package Python (vide)
│   │   ├── settings.py           # Paramètres du projet
│   │   ├── urls.py               # Routage principal
│   │   ├── wsgi.py               # Point d'entrée WSGI
│   │   └── asgi.py               # Point d'entrée ASGI
│   └── expenses/                 # Application métier
│       ├── __init__.py           # Package Python (vide)
│       ├── apps.py               # Config de l'app
│       ├── models.py             # Modèles de données (ORM)
│       ├── admin.py              # Interface d'administration
│       ├── views.py              # Vues API + Vues HTML
│       ├── urls.py               # Routage de l'app
│       ├── serializers.py        # Sérialisation DRF
│       ├── permissions.py        # Permissions personnalisées
│       ├── tests.py              # Tests (vide)
│       ├── migrations/           # Migrations de schéma
│       │   ├── __init__.py
│       │   └── 0001_initial.py
│       ├── management/           # Commandes custom
│       │   └── commands/
│       │       └── seed.py       # Injection de données
│       └── templates/
│           └── expenses/
│               ├── home.html         # Page d'accueil
│               └── event_detail.html # Bilan financier
├── http-requests/                # Fichiers de test API
│   ├── jwt.http
│   ├── events.http
│   └── expenses.http
├── docs/
│   ├── RAPPORT_REMI.md
│   └── EXPLICATIONS_PROJET.md    # Ce fichier
├── requirements.txt              # Dépendances Python
├── README.md
├── ORGANISATION.md
└── .gitignore
```

---

## 2. manage.py

**Chemin** : `djancount/manage.py`
**Rôle** : Point d'entrée principal pour toutes les commandes Django.

```python
#!/usr/bin/env python
```
- **Ligne 1** : Shebang. Indique au système d'exploitation d'utiliser l'interpréteur Python du PATH. Permet d'exécuter `./manage.py runserver` directement.

```python
"""Django's command-line utility for administrative tasks."""
```
- **Ligne 2** : Docstring du module. Convention Python pour documenter le but du fichier.

```python
import os
import sys
```
- **Lignes 3-4** : Import des modules standards.
  - `os` : Interaction avec le système d'exploitation (variables d'environnement, chemins).
  - `sys` : Accès aux arguments de ligne de commande (`sys.argv`).

```python
def main():
```
- **Ligne 6** : Définition de la fonction principale. Tout le code est encapsulé ici pour éviter l'exécution au simple import du module.

```python
    """Run administrative tasks."""
```
- **Ligne 7** : Docstring de la fonction.

```python
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
```
- **Ligne 8** : Définit la variable d'environnement `DJANGO_SETTINGS_MODULE` avec la valeur `'config.settings'`.
  - **`os.environ`** : Dictionnaire des variables d'environnement du système.
  - **`setdefault()`** : Définit la variable seulement si elle n'existe pas déjà. Cela permet de l'écraser en environnement de production.
  - **Pourquoi ?** : Django a besoin de savoir où trouver le fichier `settings.py` pour charger la configuration. Sans cette variable, Django ne sait pas quel `settings.py` utiliser.

```python
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
```
- **Lignes 10-16** : Bloc try/except qui tente d'importer `execute_from_command_line` depuis Django.
  - **`try/except`** : Gestion d'erreur. Si Django n'est pas installé, on attrape l'erreur `ImportError`.
  - **`from exc`** : Chaînage d'exceptions. Conserve l'exception originale pour le débogage.
  - **Message d'erreur** : Guide l'utilisateur sur les causes possibles (Django non installé, virtualenv non activé).

```python
    execute_from_command_line(sys.argv)
```
- **Ligne 17** : Exécute la commande passée en argument.
  - **`sys.argv`** : Liste des arguments de la ligne de commande. Ex: `['manage.py', 'runserver']`.
  - **`execute_from_command_line()`** : Fonction de Django qui parse les arguments et exécute la commande correspondante (`runserver`, `migrate`, `createsuperuser`, etc.).

```python
if __name__ == '__main__':
    main()
```
- **Lignes 19-20** : Le bloc `if __name__ == '__main__'` vérifie si le script est exécuté directement (pas importé comme module).
  - **`__name__`** : Variable spéciale Python. Valeur = `'__main__'` si le fichier est exécuté directement, ou le nom du module si importé.
  - **`main()`** : Appelle la fonction principale.

### Concepts Django associés

| Concept | Explication |
|---------|-------------|
| `DJANGO_SETTINGS_MODULE` | Variable d'environnement indiquant le module de configuration |
| `execute_from_command_line` | Fonction centrale qui routage les commandes Django |
| `sys.argv` | Liste des arguments CLI (`manage.py`, `runserver`, `migrate`, etc.) |
| Virtual env | Environnement isolé de dépendances Python (`venv/`) |

---

## 3. config/settings.py

**Chemin** : `djancount/config/settings.py`
**Rôle** : Fichier de configuration centrale. Contient TOUS les paramètres du projet Django.

### Imports

```python
from datetime import timedelta
from pathlib import Path
```
- **`timedelta`** : Utilisé pour définir la durée de vie des tokens JWT.
- **`Path`** : Classe moderne Python pour manipuler les chemins de fichiers (remplace `os.path`).

### BASE_DIR

```python
BASE_DIR = Path(__file__).resolve().parent.parent
```
- **`__file__`** : Chemin absolu du fichier `settings.py` lui-même.
- **`.resolve()`** : Résout les liens symboliques.
- **`.parent`** : Remonte au dossier parent (`config/`).
- **`.parent.parent`** : Remonte encore d'un niveau (`djancount/`).
- **Résultat** : `BASE_DIR` pointe vers la racine du projet Django (`djancount/`).
- **Usage** : Utilisé pour construire les chemins relatifs, comme `BASE_DIR / 'db.sqlite3'`.

### SECRET_KEY

```python
SECRET_KEY = 'django-insecure-8!&6(lxy(zo^p_%egle6+$$j$014&d-h#s2)91$(*!2731osls'
```
- **Rôle** : Clé secrète utilisée pour :
  - Hachage des sessions
  - Signature des tokens CSRF
  - Signature des données sensibles
- **Sécurité** : En production, cette clé doit être **secrète** et stockée en variable d'environnement. Le préfixe `django-insecure-` signale que c'est une clé de développement.
- **Comment la générer** : `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`

### DEBUG

```python
DEBUG = True
```
- **`True`** : Mode développement. Affiche les pages d'erreur détaillées, active le hot-reload, désactive la mise en cache.
- **En production** : Doit être `False`. Sans cela, les erreurs techniques sont exposées aux utilisateurs (faille de sécurité).
- **Impact** : Quand `DEBUG=False`, Django nécessite que `ALLOWED_HOSTS` contienne le domaine du site.

### ALLOWED_HOSTS

```python
ALLOWED_HOSTS = []
```
- **Rôle** : Liste des noms de domaine autorisés à servir le site.
- **Vide** = localhost uniquement (développement).
- **En production** : `['monsite.com', 'www.monsite.com']`.
- **Sécurité** : Empêche les attaques de type "Host header injection".

### INSTALLED_APPS

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'drf_spectacular',
    'expenses',
    'corsheaders'
]
```

| App | Rôle | Concepts Django |
|-----|------|-----------------|
| `django.contrib.admin` | Interface d'administration web | `ModelAdmin`, `@admin.register` |
| `django.contrib.auth` | Système d'authentification | `User`, `Group`, `Permission` |
| `django.contrib.contenttypes` | Framework de types de contenu | Introspection des modèles, Generic Relations |
| `django.contrib.sessions` | Gestion des sessions utilisateur | Cookies côté serveur, `request.session` |
| `django.contrib.messages` | Système de messages flash | Messages temporaires après une action |
| `django.contrib.staticfiles` | Servation des fichiers statiques | CSS, JS, images en développement |
| `rest_framework` | Django REST Framework | API REST, sérialiseurs, viewsets |
| `drf_spectacular` | Génération de documentation API | Swagger UI, schéma OpenAPI |
| `expenses` | Notre application métier | Modèles, vues, etc. |
| `corsheaders` | Gestion CORS | Autorise les requêtes cross-origin (frontend séparé) |

**Concept Django** : Chaque app dans `INSTALLED_APPS` peut apporter ses propres modèles, templates, management commands, etc. Django les charge automatiquement.

### MIDDLEWARE

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

**Concept Django** : Les middlewares sont des couches de traitement qui interceptent chaque requête HTTP **avant** qu'elle n'atteigne la vue, et chaque réponse **après** qu'elle soit générée. Ils sont exécutés dans l'ordre de la liste.

| Middleware | Quand | Rôle |
|-----------|-------|------|
| `SecurityMiddleware` | Requête → Vue | Ajoute des en-têtes de sécurité (HTTPS redirection, HSTS, etc.) |
| `SessionMiddleware` | Requête → Vue | Charge et sauvegarde les sessions utilisateur (cookies) |
| `CommonMiddleware` | Requête → Vue | Gère les URLs sans slash final, les Content-Length, les Range headers |
| `CsrfViewMiddleware` | Requête → Vue | Valide les tokens CSRF pour les formulaires POST/PUT/DELETE |
| `AuthenticationMiddleware` | Requête → Vue | Attache `request.user` à chaque requête en vérifiant la session |
| `MessageMiddleware` | Requête → Vue | Gère les messages flash (messages temporaires après une action) |
| `XFrameOptionsMiddleware` | Réponse → Client | Ajoute l'en-tête `X-Frame-Options: DENY` pour empêcher le clickjacking |

**Ordre important** :
1. `SessionMiddleware` doit être avant `AuthenticationMiddleware` (car l'auth dépend de la session).
2. `CsrfViewMiddleware` doit être après `SessionMiddleware` (car le token CSRF dépend de la session).

### TEMPLATES

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

| Option | Rôle |
|--------|------|
| `BACKEND` | Moteur de templates utilisé (le moteur Django par défaut) |
| `DIRS` | Répertoires supplémentaires pour chercher les templates (vide ici) |
| `APP_DIRS = True` | Cherche les templates dans `<app>/templates/` de chaque app |
| `context_processors` | Fonctions qui ajoutent des variables au contexte de tous les templates |

**Context processors** :
- `request` : Ajoute `{{ request }}` au template (l'objet HTTP request).
- `auth` : Ajoute `{{ user }}` (l'utilisateur connecté) et `{{ perms }}` (ses permissions).
- `messages` : Ajoute `{{ messages }}` (les messages flash).

**Concept Django** : Les templates sont des fichiers HTML avec une syntaxe spéciale (`{{ variable }}`, `{% tag %}`). Django les recherche dans l'ordre : `DIRS` d'abord, puis `APP_DIRS`.

### WSGI_APPLICATION

```python
WSGI_APPLICATION = 'config.wsgi.application'
```
- Pointe vers le module WSGI dans `config/wsgi.py`.
- Utilisé par les serveurs de production (Gunicorn, uWSGI) pour charger l'application.

### REST_FRAMEWORK

```python
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'DjanCount API',
    'DESCRIPTION': 'API REST de gestion de depensees partagees (type Tricount)',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}
```

**Concept DRF** : Ces settings s'appliquent à TOUTES les vues DRF du projet.

| Setting | Valeur | Rôle |
|---------|--------|------|
| `DEFAULT_AUTHENTICATION_CLASSES` | `JWTAuthentication` | Les utilisateurs s'authifient avec un token JWT (pas de session) |
| `DEFAULT_PERMISSION_CLASSES` | `IsAuthenticatedOrReadOnly` | GET = public, POST/PUT/DELETE = authentification requise |
| `DEFAULT_SCHEMA_CLASS` | `drf_spectacular.openapi.AutoSchema` | Génère le schéma OpenAPI pour Swagger |

**JWT (JSON Web Token)** : Mécanisme d'authentification stateless. L'utilisateur envoie son token dans l'en-tête `Authorization: Bearer <token>`. Pas de stockage côté serveur.

### SIMPLE_JWT

```python
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}
```

| Token | Durée | Rôle |
|-------|-------|------|
| **Access Token** | 1 heure | Utilisé pour accéder aux endpoints protégés. Court pour la sécurité. |
| **Refresh Token** | 1 jour | Utilisé pour obtenir un nouvel access token sans re-saisir le mot de passe. |

**Flux JWT** :
1. L'utilisateur envoie `POST /api/token/` avec username + password.
2. Le serveur renvoie `access` et `refresh` tokens.
3. Le client utilise `access` dans l'en-tête `Authorization: Bearer <access>`.
4. Quand `access` expire, il envoie `POST /api/token/refresh/` avec le `refresh` token.
5. Le serveur renvoie un nouveau `access` token.

### DATABASES

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

| Option | Valeur | Rôle |
|--------|--------|------|
| `ENGINE` | `django.db.backends.sqlite3` | Moteur SQLite (base fichier) |
| `NAME` | `BASE_DIR / 'db.sqlite3'` | Chemin vers le fichier de base |

**SQLite** : Base de données fichier unique, sans serveur. Parfaite pour le développement. En production, on utiliserait PostgreSQL (`django.db.backends.postgresql`).

**Concept Django** : Le moteur de base de données est abstrait. On change le `ENGINE` et Django génère le bon SQL (SQLite, PostgreSQL, MySQL, etc.).

### AUTH_PASSWORD_VALIDATORS

```python
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]
```

| Validateur | Rôle |
|------------|------|
| `UserAttributeSimilarityValidator` | Empêche les mots de passe trop similaires au nom d'utilisateur |
| `MinimumLengthValidator` | Impose une longueur minimale (8 caractères par défaut) |
| `CommonPasswordValidator` | Empêche les mots de passe trop communs ("password123", "123456") |
| `NumericPasswordValidator` | Empêche les mots de passe entièrement numériques |

**Concept Django** : Ces validateurs sont appliqués automatiquement lors de `User.objects.create_user()` et du changement de mot de passe.

### Internationalisation

```python
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
```

| Setting | Rôle |
|---------|------|
| `LANGUAGE_CODE` | Langue par défaut de l'interface admin |
| `TIME_ZONE` | Fuseau horaire par défaut |
| `USE_I18N` | Active l'internationalisation (translations) |
| `USE_TZ = True` | Stocke les dates en UTC dans la base, convertit au fuseau local à l'affichage |

**`USE_TZ = True`** : IMPORTANT. Évite les problèmes de fuseau horaire. Les dates sont stockées en UTC et converties automatiquement.

### STATIC_URL

```python
STATIC_URL = 'static/'
```
- URL de base pour les fichiers statiques (CSS, JS, images).
- En développement, Django les sert via `django.contrib.staticfiles`.
- En production, on les place sur un CDN ou un serveur Nginx.

### DEFAULT_AUTO_FIELD

```python
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
```
- **`BigAutoField`** : Entier 64-bit auto-incrémenté (au lieu de 32-bit par défaut).
- **Pourquoi ?** : Les `AutoField` 32-bit sont limités à ~2 milliards. `BigAutoField` évite ce problème pour les très grandes tables.
- **Impact** : Tous les modèles créés après auront une clé primaire `BigAutoField` au lieu de `AutoField`.

---

## 4. config/urls.py

**Chemin** : `djancount/config/urls.py`
**Rôle** : Fichier de routage principal de tout le projet.

```python
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
```

- **`admin`** : L'interface d'administration Django.
- **`path`** : Fonction pour définir une route URL.
- **`include`** : Fonction pour déléguer des sous-chemins à une autre app.
- **`TokenObtainPairView`** : Vue DRF qui génère un couple de tokens JWT (access + refresh).
- **`TokenRefreshView`** : Vue DRF qui rafraîchit un access token expiré.
- **`SpectacularAPIView`** : Vue qui génère le schéma OpenAPI en JSON/YAML.
- **`SpectacularSwaggerView`** : Vue qui affiche l'interface Swagger UI (documentation interactive).

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('expenses.urls')),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
```

| Route | Destination | Rôle |
|-------|-------------|------|
| `admin/` | Interface admin Django | Gestion visuelle des données |
| `''` (racine) | `expenses.urls` | Redirige tout le reste vers l'app expenses |
| `api/token/` | `TokenObtainPairView` | `POST` avec username+password → retourne les tokens JWT |
| `api/token/refresh/` | `TokenRefreshView` | `POST` avec refresh token → retourne un nouvel access token |
| `api/schema/` | `SpectacularAPIView` | Génère le schéma OpenAPI brut (JSON) |
| `api/docs/` | `SpectacularSwaggerView` | Interface Swagger UI interactive |

**Concept Django** : `path('', include('expenses.urls'))` signifie "pour toute URL qui commence par la racine, passe la main au fichier `expenses/urls.py`". C'est le principe de la **décomposition par apps**.

**`as_view()`** : Convertit une classe en fonction que Django peut appeler comme une vue. C'est le pattern "Class-Based View" de Django.

**`name="token_obtain_pair"`** : Nom unique pour cette URL. Permet de la retrouver avec `{% url 'token_obtain_pair' %}` dans les templates ou `reverse('token_obtain_pair')` dans le code.

---

## 5. config/wsgi.py & asgi.py

### wsgi.py

**Rôle** : Point d'entrée pour les serveurs web **synchrones** (HTTP classique).

```python
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
application = get_wsgi_application()
```

| Élément | Rôle |
|---------|------|
| `get_wsgi_application()` | Crée l'objet application WSGI que le serveur appellera |
| `application` | Variable standard WSGI que le serveur importe |
| `DJANGO_SETTINGS_MODULE` | Même variable que dans `manage.py` |

**WSGI (Web Server Gateway Interface)** : Standard Python pour communiquer entre un serveur web et une application Python. Utilisé par Gunicorn, uWSGI, Apache mod_wsgi.

**Comment ça marche** :
1. Le serveur web (ex: Gunicorn) reçoit une requête HTTP.
2. Il appelle `application(environ, start_response)`.
3. Django traite la requête et retourne la réponse.

### asgi.py

**Rôle** : Point d'entrée pour les serveurs web **asynchrones** (WebSocket, HTTP/2).

```python
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
application = get_asgi_application()
```

**ASGI (Asynchronous Server Gateway Interface)** : Standard moderne pour les applications Python asynchrones. Supporte HTTP, WebSocket, et les connexions longues.

**Différences WSGI vs ASGI** :

| Critère | WSGI | ASGI |
|---------|------|------|
| Protocole | HTTP synchrone | HTTP + WebSocket |
| Performance | Requête = 1 thread | Requête = 1 coroutine (async) |
| Serveurs | Gunicorn, uWSGI | Daphne, Uvicorn |
| Usage | Sites web classiques | Chat temps réel, notifications push |

Dans ce projet, ASGI est présent pour la complétude mais le projet utilise principalement WSGI.

---

## 6. expenses/apps.py

**Chemin** : `djancount/expenses/apps.py`
**Rôle** : Configuration de l'application Django `expenses`.

```python
from django.apps import AppConfig

class ExpensesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'expenses'
```

| Attribut | Rôle |
|----------|------|
| `name = 'expenses'` | Nom du package Python (correspond au nom du dossier) |
| `default_auto_field` | Type de clé primaire par défaut pour les modèles de cette app |

**Concept Django** : `AppConfig` est la classe de base pour la configuration d'une app. Elle permet de :
- Définir les métadonnées de l'app.
- Exécuter du code au démarrage (`ready()` method).
- Définir le type de clé primaire par défaut.

**`BigAutoField`** : Clé primaire entier 64-bit auto-incrémenté. Évite les problèmes de dépassement de capacité pour les très grandes tables.

**`__init__.py`** (dossier `expenses/`) : Fichier vide qui indique à Python que `expenses/` est un **package** importable.

---

## 7. expenses/models.py

**Chemin** : `djancount/expenses/models.py`
**Rôle** : Définit la structure de la base de données via l'ORM Django. C'est le cœur du modèle de données.

### Imports

```python
from django.db import models
from django.contrib.auth.models import User
```

- **`models`** : Module principal de l'ORM Django. Contient tous les types de champs (`CharField`, `TextField`, etc.).
- **`User`** : Modèle d'utilisateur natif de Django (`django.contrib.auth.models.User`). Fournit `username`, `password`, `email`, `first_name`, `last_name`, `is_staff`, etc.

### Modèle Event

```python
class Event(models.Model):
```
- **`models.Model`** : Classe de base. Hérite de toutes les fonctionnalités ORM (requêtes, sauvegarde, suppression, etc.).
- **Convention** : Chaque modèle devient une table en base. `Event` → table `expenses_event`.

```python
    name = models.CharField(max_length=200)
```
- **`CharField`** : Champ texte court (équivalent `VARCHAR` en SQL).
- **`max_length=200`** : Longueur maximale obligatoire. En SQL : `VARCHAR(200) NOT NULL`.
- **Obligatoire** par défaut (pas de `blank=True`).

```python
    description = models.TextField(blank=True)
```
- **`TextField`** : Champ texte long (équivalent `TEXT` en SQL). Pas de limite de longueur.
- **`blank=True`** : Le champ est optionnel dans les formulaires (validation Django). En SQL : pas de `NOT NULL`.

```python
    participants = models.ManyToManyField(User, related_name="events")
```
- **`ManyToManyField`** : Relation plusieurs-à-plusieurs. Un événement a plusieurs participants, un utilisateur peut participer à plusieurs événements.
- **`User`** : Le modèle cible de la relation.
- **`related_name="events"`** : Nom de la relation inverse. `user.events.all()` retourne tous les événements d'un utilisateur.
- **Table intermédiaire** : Django crée automatiquement une table `expenses_event_participants` avec deux colonnes : `event_id` et `user_id`.

**Concept Django** : `ManyToManyField` ne crée PAS de colonne dans la table `Event`. Il crée une **table de jointure** séparée.

```python
    def __str__(self):
        return self.name
```
- **`__str__`** : Représentation textuelle de l'objet. Affiché dans :
  - L'interface admin
  - Le shell Django
  - Les templates (`{{ event }}` appelle `str(event)`)
  - Les serializers (si non spécifié autrement)

### Modèle Expense

```python
class Expense(models.Model):
```

```python
    title = models.CharField(max_length=200)
```
- Champ texte court, obligatoire. Ex: "Essence", "Courses", "Restaurant".

```python
    amount = models.DecimalField(max_digits=10, decimal_places=2)
```
- **`DecimalField`** : Champ numérique à précision fixe (équivalent `DECIMAL` en SQL).
- **`max_digits=10`** : Nombre total de chiffres (avant + après la virgule).
- **`decimal_places=2`** : Nombre de chiffres après la virgule.
- **Exemple** : `99999999.99` (8 chiffres avant + 2 après = 10 total).
- **Pourquoi pas `FloatField` ?** : `FloatField` utilise des flottants IEEE 754 qui ont des erreurs d'arrondi. `DecimalField` utilise des décimaux exacts, essentiels pour l'argent.

```python
    payer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="expenses_paid")
```
- **`ForeignKey`** : Relation plusieurs-vers-un. Chaque dépense a un seul payeur.
- **`on_delete=models.CASCADE`** : Si le `User` est supprimé, toutes ses dépenses sont supprimées aussi (suppression en cascade).
- **`related_name="expenses_paid"`** : `user.expenses_paid.all()` retourne toutes les dépenses payées par cet utilisateur.

```python
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="expenses")
```
- **`ForeignKey`** : Chaque dépense appartient à un seul événement.
- **`on_delete=models.CASCADE`** : Si l'`Event` est supprimé, toutes ses dépenses sont supprimées.
- **`related_name="expenses"`** : `event.expenses.all()` retourne toutes les dépenses d'un événement.

```python
    date = models.DateField(auto_now_add=True)
```
- **`DateField`** : Champ date (sans heure).
- **`auto_now_add=True`** : La date est définie automatiquement à la date de création de l'objet. Non modifiable.
- **En SQL** : `DATE NOT NULL` avec valeur par défaut.

```python
    def __str__(self):
        return f"{self.title} - {self.amount}€"
```
- Représentation textuelle : "Essence - 45.50€".

### Résumé des relations

```
User (1) ──────────< (N) Event          (ManyToMany via table intermédiaire)
   │                      │
   │                      │
   └──── (1) ──< (N) Expense >── (N) ── (1) Event
         (payer)                    (event)
```

| Relation | Type | Table de jointure ? |
|----------|------|---------------------|
| Event ↔ User (participants) | ManyToManyField | Oui (`expenses_event_participants`) |
| Expense → User (payer) | ForeignKey | Non (colonne `payer_id` dans `Expense`) |
| Expense → Event (event) | ForeignKey | Non (colonne `event_id` dans `Expense`) |

---

## 8. expenses/admin.py

**Chemin** : `djancount/expenses/admin.py`
**Rôle** : Configure l'interface d'administration Django pour visualiser et gérer les données.

```python
from django.contrib import admin
from .models import Event, Expense
```

```python
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)
    filter_horizontal = ("participants",)
```

| Option | Valeur | Rôle |
|--------|--------|------|
| `@admin.register(Event)` | Décorateur | Enregistre `EventAdmin` pour le modèle `Event` |
| `list_display` | `("name", "description")` | Colonnes affichées dans la vue liste |
| `search_fields` | `("name",)` | Ajoute une barre de recherche par nom |
| `filter_horizontal` | `("participants",)` | Widget de sélection M2M avec deux listes (gauche/droite) |

**`@admin.register(Event)`** : Équivalent de `admin.site.register(Event, EventAdmin)`. Décorateur moderne et plus lisible.

**`filter_horizontal`** : Pour les `ManyToManyField`, affiche deux listes avec des flèches pour ajouter/retirer des éléments. Beaucoup plus ergonomique qu'un `<select multiple>`.

```python
@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("title", "amount", "payer", "event", "date")
    list_filter = ("event", "payer")
    search_fields = ("title",)
```

| Option | Valeur | Rôle |
|--------|--------|------|
| `list_display` | 5 colonnes | Affiche toutes les infos utiles dans la liste |
| `list_filter` | `("event", "payer")` | Filtres latéraux pour filtrer par événement ou payeur |
| `search_fields` | `("title",)` | Recherche par titre de dépense |

**Concept Django** : L'admin Django est généré automatiquement à partir des modèles. On le personnalise en définissant des classes `ModelAdmin` avec des options d'affichage.

---

## 9. expenses/serializers.py

**Chemin** : `djancount/expenses/serializers.py`
**Rôle** : Convertit les objets Python en JSON (et inversement) pour l'API REST. Effectue aussi la validation des données.

### Imports

```python
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Event, Expense
```

### EventSerializer

```python
class EventSerializer(serializers.ModelSerializer):
```
- **`ModelSerializer`** : Classe DRF qui génère automatiquement les champs à partir du modèle Django. Équivalent de définir manuellement chaque champ.

```python
    participants_count = serializers.IntegerField(source="participants.count", read_only=True)
    expenses_count = serializers.IntegerField(source="expenses.count", read_only=True)
```
- **`IntegerField`** : Champ entier.
- **`source="participants.count"`** : La valeur est calculée via `event.participants.count()` (comptage automatique).
- **`read_only=True`** : Le champ est inclus dans les réponses GET mais ignoré lors des créations/mises à jour POST/PUT/PATCH.
- **Utilité** : Évite de charger tous les participants/dépenses juste pour les compter.

```python
    class Meta:
        model = Event
        fields = [
            "id", "name", "description", "participants",
            "participants_count", "expenses_count"
        ]
        read_only_fields = ["id"]
```
- **`model = Event`** : Lie le sérialiseur au modèle `Event`.
- **`fields`** : Liste des champs à inclure dans le JSON.
- **`read_only_fields = ["id"]`** : L'identifiant est toujours en lecture seule (généré par la base).

**JSON de sortie** :
```json
{
    "id": 1,
    "name": "Week-end à la mer",
    "description": "Trois jours à Biarritz",
    "participants": [2, 3, 4],
    "participants_count": 3,
    "expenses_count": 3
}
```

### ExpenseSerializer

```python
class ExpenseSerializer(serializers.ModelSerializer):
    payer_name = serializers.CharField(source="payer.username", read_only=True)
    event_name = serializers.CharField(source="event.name", read_only=True)
```
- **`payer_name`** : Champ calculé. Affiche le nom d'utilisateur du payeur (pas son ID).
- **`event_name`** : Champ calculé. Affiche le nom de l'événement.
- **`source="payer.username"`** : Accède à `expense.payer.username`.

```python
    class Meta:
        model = Expense
        fields = [
            "id", "title", "amount", "payer", "payer_name",
            "event", "event_name", "date"
        ]
        read_only_fields = ["id", "date"]
```
- **`date`** en `read_only_fields` : La date est définie automatiquement (`auto_now_add=True`), pas modifiable via l'API.

### Validation : validate_amount

```python
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Le montant doit etre strictement positif.")
        return value
```

**Concept DRF** : La méthode `validate_<fieldname>()` est appelée **automatiquement** pour valider un champ spécifique.

| Étape | Explication |
|-------|-------------|
| `self` | Le sérialiseur lui-même |
| `value` | La valeur du champ `amount` envoyée par le client |
| `if value <= 0` | Vérification : le montant doit être > 0 |
| `raise ValidationError` | Si invalide, lève une erreur qui sera retournée en JSON 400 |
| `return value` | Si valide, retourne la valeur (éventuellement transformée) |

**Réponse d'erreur** (HTTP 400) :
```json
{
    "amount": ["Le montant doit etre strictement positif."]
}
```

### Validation : validate (globale)

```python
    def validate(self, attrs):
        payer = attrs.get('payer', getattr(self.instance, 'payer', None))
        event = attrs.get('event', getattr(self.instance, 'event', None))

        if event and payer and payer not in event.participants.all():
            raise serializers.ValidationError(
                {"payer": "Le payeur doit faire partie des participants de cet evenement."}
            )
        return attrs
```

**Concept DRF** : La méthode `validate()` est la validation **globale**, appelée après toutes les validations de champs individuels.

| Ligne | Explication |
|-------|-------------|
| `attrs.get('payer', ...)` | Récupère le payer des données envoyées, ou de l'objet existant (pour PATCH) |
| `getattr(self.instance, 'payer', None)` | Si PATCH, le champ peut manquer. On récupère la valeur actuelle de l'objet |
| `payer not in event.participants.all()` | Vérifie que le payeur est bien dans la liste des participants |
| `raise ValidationError({"payer": ...})` | Erreur attachée au champ `payer` spécifiquement |

**Cas d'usage** : Un utilisateur ne peut pas créer une dépense pour un événement dont il ne fait pas partie.

**Pourquoi `getattr(self.instance, ...)` ?** : En mode PATCH (mise à partielle), le client peut envoyer uniquement le champ `amount` sans `payer` ni `event`. Il faut donc récupérer les valeurs actuelles de l'objet existant.

---

## 10. expenses/permissions.py

**Chemin** : `djancount/expenses/permissions.py`
**Rôle** : Définit des règles d'accès personnalisées pour l'API REST.

```python
"""Permissions metier propres aux ressources de l'application expenses."""
from rest_framework.permissions import IsAuthenticated
```

- Docstring décrivant le module.
- **`IsAuthenticated`** : Permission DRF de base. Autorise uniquement les utilisateurs authentifiés.

### IsEventParticipant

```python
class IsEventParticipant(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.participants.filter(pk=request.user.pk).exists()
```

**Concept DRF** : Les permissions sont des classes avec une méthode `has_permission()` (accès général) et/ou `has_object_permission()` (accès à un objet spécifique).

| Ligne | Explication |
|-------|-------------|
| `class IsEventParticipant(IsAuthenticated)` | Hérite de `IsAuthenticated` : d'abord vérifie que l'utilisateur est connecté |
| `has_object_permission(self, request, view, obj)` | Appelé pour VÉRIFIER l'accès à un objet spécifique |
| `request.user.is_staff` | Les administrateurs Django ont toujours accès |
| `obj.participants.filter(pk=request.user.pk).exists()` | Vérifie si l'utilisateur est dans la liste des participants |
| `.exists()` | Retourne `True/False` sans charger l'objet User (optimisé) |

**Flux** :
1. Requête arrive → `IsAuthenticated` vérifie le token JWT.
2. Si OK → `has_object_permission` vérifie que l'utilisateur est participant.
3. Si OK → La vue s'exécute.
4. Si non → Réponse 403 Forbidden.

### IsPayerOrEventParticipant

```python
class IsPayerOrEventParticipant(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_staff
            or obj.payer_id == request.user.pk
            or obj.event.participants.filter(pk=request.user.pk).exists()
        )
```

**Qui a accès à une dépense ?**

| Condition | Rôle |
|-----------|------|
| `request.user.is_staff` | Administrateur Django |
| `obj.payer_id == request.user.pk` | La personne qui a payé |
| `obj.event.participants.filter(...).exists()` | Un participant de l'événement |

**Note** : `obj.payer_id` est plus efficace que `obj.payer.pk` car il évite une requête SQL supplémentaire (le champ `payer_id` est déjà chargé).

---

## 11. expenses/views.py

**Chemin** : `djancount/expenses/views.py`
**Rôle** : Contient toute la logique métier — les vues API REST (ViewSets) et la vue HTML (fonction).

### Imports

```python
from django.db.models import Q
```
- **`Q`** : Objet de requête complexe. Permet les opérations OR dans les filtres Django ORM.
- Sans `Q`, on ne peut faire que des filtres AND.

```python
from django.shortcuts import render, get_object_or_404
```
- **`render`** : Rend un template HTML avec un contexte de données.
- **`get_object_or_404`** : Récupère un objet ou renvoie une page 404 (page non trouvée).

```python
from rest_framework import viewsets
```
- **`viewsets`** : Module DRF contenant les ViewSets (vues CRUD complètes).

```python
from .models import Event, Expense
from .serializers import EventSerializer, ExpenseSerializer
from .permissions import IsEventParticipant, IsPayerOrEventParticipant
```
- Imports des modèles, sérialiseurs et permissions de l'app courante.

### Vue HTML : homepage_view

```python
def homepage_view(request):
    from .models import Event
    events = Event.objects.prefetch_related("participants").all()
    return render(request, 'expenses/home.html', {'events': events})
```

| Ligne | Explication |
|-------|-------------|
| `def homepage_view(request)` | Fonction Django classique. `request` = l'objet HTTP. |
| `from .models import Event` | Import local (évite les imports circulaires). |
| `Event.objects.prefetch_related("participants").all()` | Récupère tous les événements avec les participants pré-chargés (optimisation N+1). |
| `render(request, 'expenses/home.html', {'events': events})` | Rend le template `home.html` avec la liste des événements dans le contexte. |

### EventViewSet

```python
class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.prefetch_related("participants", "expenses").all()
    serializer_class = EventSerializer
    permission_classes = [IsEventParticipant]
```

**Concept DRF — ModelViewSet** : Un `ModelViewSet` est une vue complète qui fournit automatiquement les 6 opérations CRUD :

| Méthode HTTP | URL | Action DRF | Rôle |
|-------------|-----|------------|------|
| `GET` | `/api/events/` | `list` | Lister tous les événements |
| `POST` | `/api/events/` | `create` | Créer un événement |
| `GET` | `/api/events/{id}/` | `retrieve` | Détail d'un événement |
| `PUT` | `/api/events/{id}/` | `update` | Modification complète |
| `PATCH` | `/api/events/{id}/` | `partial_update` | Modification partielle |
| `DELETE` | `/api/events/{id}/` | `destroy` | Supprimer un événement |

| Attribut | Rôle |
|----------|------|
| `queryset` | La requête de base (tous les événements avec participants et dépenses pré-chargés) |
| `serializer_class` | Le sérialiseur à utiliser pour la conversion JSON |
| `permission_classes` | Les permissions à vérifier |

**`prefetch_related("participants", "expenses")`** : Optimisation N+1. Au lieu de faire 1 requête pour les participants + 1 par événement, Django fait 3 requêtes au total (1 pour les événements, 1 pour tous les participants, 1 pour toutes les dépenses).

```python
    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset
        return self.queryset.filter(participants=self.request.user).distinct()
```

**Concept DRF** : `get_queryset()` est appelé pour chaque requête pour filtrer les objets accessibles.

| Cas | Résultat |
|-----|----------|
| Utilisateur staff | Voit TOUS les événements |
| Utilisateur normal | Voit uniquement les événements où il est participant |

**`.distinct()`** : Élimine les doublons. Sans cela, un événement avec 3 participants pourrait apparaître 3 fois dans les résultats.

### ExpenseViewSet

```python
class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.select_related("payer", "event").all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsPayerOrEventParticipant]
```

**`select_related("payer", "event")`** : Joint SQL. Au lieu de faire 1 requête par dépense pour charger le payeur et l'événement, une seule requête `JOIN` est faite.

**Différence `select_related` vs `prefetch_related`** :
| Méthode | Usage | Type de relation |
|---------|-------|------------------|
| `select_related` | ForeignKey, OneToOne | Jointure SQL (1 requête) |
| `prefetch_related` | ManyToMany, Reverse FK | Requêtes séparées (3 requêtes max) |

```python
    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset
        return self.queryset.filter(
            Q(payer=self.request.user) | Q(event__participants=self.request.user)
        ).distinct()
```

**Ligne 51-53 — Filtre complexe avec Q** :

```python
Q(payer=self.request.user) | Q(event__participants=self.request.user)
```

- **`Q(payer=self.request.user)`** : Dépenses où l'utilisateur est le payeur.
- **`|`** : Opérateur OR.
- **`Q(event__participants=self.request.user)`** : Dépenses dont l'événement contient l'utilisateur comme participant. La double记者 `__` traverse la relation ForeignKey → ManyToManyField.
- **Résultat** : L'utilisateur voit les dépenses qu'il a payées OU celles des événements auxquels il participe.

**`__` (double underscore)** : Syntaxe Django ORM pour traverser les relations. `event__participants` signifie "les participants de l'événement de cette dépense".

### Vue HTML : event_detail_view

```python
def event_detail_view(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    participants = list(event.participants.all())
    expenses = event.expenses.select_related("payer").all()
```

| Ligne | Explication |
|-------|-------------|
| `def event_detail_view(request, event_id)` | Fonction Django classique. `request` = l'objet HTTP. `event_id` = paramètre d'URL. |
| `get_object_or_404(Event, pk=event_id)` | Récupère l'événement ou renvoie une 404. `pk` = clé primaire (id). |
| `list(event.participants.all())` | Convertit le QuerySet en liste Python (pour l'indexation). |
| `event.expenses.select_related("payer").all()` | Récupère toutes les dépenses avec le payeur en une seule requête SQL. |

---

#### ALGORITHME DU BILAN FINANCIER — LIGNE PAR LIGNE

C'est le cœur de la logique métier. L'algorithme calcule qui doit quoi à qui, en minimisant le nombre de transactions.

##### ÉTAPE 1 : Calcul du total et de la part par personne (lignes 65-66)

```python
    total_expenses = sum(expense.amount for expense in expenses)
```
- **`sum()`** : Fonction Python qui additionne tous les éléments d'un itérable.
- **`expense.amount for expense in expenses`** : Generator expression. Itère sur toutes les dépenses et extrait le champ `amount`.
- **Résultat** : La somme totale de toutes les dépenses de l'événement.
- **Exemple** : Si 3 dépenses de 45.50€, 78.20€, 120.00€ → `total_expenses = 243.70`

```python
    part_per_person = total_expenses / len(participants) if participants else 0
```
- **`len(participants)`** : Nombre de participants à l'événement.
- **`if participants else 0`** : Protection contre la division par zéro. Si pas de participants, `part_per_person = 0`.
- **Résultat** : Ce que chaque personne devrait théoriquement payer.
- **Exemple** : `243.70 / 3 = 81.23€` par personne.

##### ÉTAPE 2 : Initialisation des soldes (lignes 68-70)

```python
    balances = {}
    for participant in participants:
        balances[participant.first_name] = -part_per_person
```

- **`balances = {}`** : Dictionnaire qui stocke le solde de chaque participant.
- **Boucle** : Pour chaque participant, on initialise son solde à **-part_per_person**.
- **Pourquoi négatif ?** : Chaque personne "doit" sa part. On part du principe que personne n'a encore payé. Le solde négatif représente ce qu'on doit.
- **Résultat** : Si 3 participants et part = 81.23€ :
  ```
  balances = {
      "Alice": -81.23,
      "Bob": -81.23,
      "Chloe": -81.23
  }
  ```

##### ÉTAPE 3 : Mise à jour des soldes avec les paiements réels (lignes 72-75)

```python
    for expense in expenses:
        payer_name = expense.payer.first_name
        if payer_name in balances:
            balances[payer_name] += expense.amount
```

- **Boucle** : Pour chaque dépense...
- **`expense.payer.first_name`** : Récupère le prénom du payeur (objet ForeignKey → objet User → attribut first_name).
- **`if payer_name in balances`** : Vérification de sécurité. Si le payeur n'est pas dans les participants (ne devrait pas arriver avec la validation, mais on est prudent), on l'ignore.
- **`balances[payer_name] += expense.amount`** : Ajoute le montant payé au solde du payeur.

**Logique** :
- Le solde partait à **-81.23** (ce qu'on doit).
- Si Alice a payé 45.50€, son solde devient : `-81.23 + 45.50 = -35.73`.
- Alice a encore "une dette" de 35.73€ (elle n'a pas payé sa part complète).

**Exemple complet après les 3 dépenses** :

```
Dépenses :
  - Alice a payé 45.50€ → balances["Alice"] = -81.23 + 45.50 = -35.73
  - Bob a payé 78.20€ → balances["Bob"] = -81.23 + 78.20 = -3.03
  - Chloe a payé 120.00€ → balances["Chloe"] = -81.23 + 120.00 = +38.77
```

**Interprétation** :
- Alice : **-35.73** → Elle doit 35.73€ (débiteur).
- Bob : **-3.03** → Il doit 3.03€ (débiteur).
- Chloe : **+38.77** → On lui doit 38.77€ (créancier).

Vérification : `-35.73 + (-3.03) + 38.77 = 0.01` (arrondi). La somme des soldes est toujours ≈ 0.

##### ÉTAPE 4 : Classification en débiteurs et créanciers (lignes 77-85)

```python
    transactions = []
    debtors = []
    creditors = []
```
- **`transactions`** : Liste des transactions à effectuer (résultat final).
- **`debtors`** : Liste des personnes qui doivent de l'argent (solde négatif).
- **`creditors`** : Liste des personnes à qui on doit de l'argent (solde positif).

```python
    for name, balance in balances.items():
        if balance < -0.01:
            debtors.append([name, -balance])
        elif balance > 0.01:
            creditors.append([name, balance])
```

**Pourquoi `-0.01` et `0.01` ?** : Seuil de tolérance pour les erreurs d'arrondi. Un solde de -0.005€ est considéré comme "équilibré" (0€).

**`debtors.append([name, -balance])`** : Note le **-** devant `balance`. Si le solde est -35.73, on stocke [name, 35.73] (montant positif = montant dû).

**`creditors.append([name, balance])`** : Le solde est déjà positif, on le stocke tel quel.

**Résultat** :
```
debtors = [["Alice", 35.73], ["Bob", 3.03]]
creditors = [["Chloe", 38.77]]
```

##### ÉTAPE 5 : Algorithme glouton à deux pointeurs (lignes 87-105)

```python
    i = 0
    j = 0
```
- **`i`** : Index pour parcourir les débiteurs.
- **`j`** : Index pour parcourir les créanciers.

```python
    while i < len(debtors) and j < len(creditors):
```
- **Boucle tant qu'il reste des débiteurs ET des créanciers** à traiter.
- Si l'un des deux listes est épuisée, on s'arrête (les comptes sont équilibrés).

```python
        amount = min(debtors[i][1], creditors[j][1])
```
- **`min()`** : Prend le minimum entre ce que le débiteur doit et ce que le créancier attend.
- **Pourquoi ?** : On ne peut pas transférer plus que ce que le débiteur doit, ni plus que ce que le créancier attend.
- **Exemple** : `min(35.73, 38.77) = 35.73`. Alice doit 35.73€, Chloe attend 38.77€. On transfère 35.73€.

```python
        transactions.append({
            'from': debtors[i][0],
            'to': creditors[j][0],
            'amount': round(amount, 2)
        })
```
- **`transactions.append()`** : Ajoute une transaction à la liste.
- **`'from'`** : Nom du débiteur (celui qui paie).
- **`'to'`** : Nom du créancier (celui qui reçoit).
- **`round(amount, 2)`** : Arrondi à 2 décimales (pour l'affichage).
- **Résultat** : `{'from': 'Alice', 'to': 'Chloe', 'amount': 35.73}`

```python
        debtors[i][1] -= amount
        creditors[j][1] -= amount
```
- **Décrémentation** : Réduit les montants restants.
- **Alice** : `35.73 - 35.73 = 0` → Elle a tout remboursé.
- **Chloe** : `38.77 - 35.73 = 3.04` → Il lui reste 3.04€ à recevoir.

```python
        if debtors[i][1] <= 0.01:
            i += 1
        if creditors[j][1] <= 0.01:
            j += 1
```
- **Seuil 0.01** : Tolérance d'arrondi. Si le montant restant est ≤ 0.01, on considère que c'est payé.
- **`i += 1`** : Passe au débiteur suivant (Alice est "réglée").
- **`j += 1`** : Passe au créancier suivant (Chloe n'est PAS encore réglée, donc `j` n'augmente pas ici).
- **Note** : Les deux `if` sont indépendants (pas `elif`). Les deux peuvent être vrais en même temps si les montants sont égaux.

##### ÉTAPE 6 : Construction du contexte et rendu (lignes 107-117)

```python
    context = {
        'event': event,
        'participants': participants,
        'expenses': expenses,
        'total': total_expenses,
        'part': part_per_person,
        'balances': balances,
        'transactions': transactions
    }

    return render(request, 'expenses/event_detail.html', context)
```

- **`context`** : Dictionnaire des données envoyées au template.
- **`render()`** : Rend le template HTML avec le contexte.
  - `request` : L'objet HTTP (requis par Django).
  - `'expenses/event_detail.html'` : Chemin du template (cherché dans `expenses/templates/`).
  - `context` : Données disponibles dans le template via `{{ variable }}`.

##### Exemple complet d'exécution

**Données d'entrée** :
```
Événement : "Week-end à la mer"
Participants : Alice, Bob, Chloe
Dépenses :
  - Essence : 45.50€ (payé par Alice)
  - Courses : 78.20€ (payé par Bob)
  - Restaurant : 120.00€ (payé par Chloe)
```

**Exécution pas à pas** :

```
1. total_expenses = 45.50 + 78.20 + 120.00 = 243.70
2. part_per_person = 243.70 / 3 = 81.23

3. Initialisation :
   balances = {"Alice": -81.23, "Bob": -81.23, "Chloe": -81.23}

4. Mise à jour des paiements :
   Alice a payé 45.50 → balances["Alice"] = -81.23 + 45.50 = -35.73
   Bob a payé 78.20 → balances["Bob"] = -81.23 + 78.20 = -3.03
   Chloe a payé 120.00 → balances["Chloe"] = -81.23 + 120.00 = +38.77

5. Classification :
   debtors = [["Alice", 35.73], ["Bob", 3.03]]
   creditors = [["Chloe", 38.77]]

6. Algorithme glouton :
   Tour 1 : i=0, j=0
     amount = min(35.73, 38.77) = 35.73
     Transaction : Alice → Chloe : 35.73€
     debtors[0][1] = 35.73 - 35.73 = 0 → i passe à 1
     creditors[0][1] = 38.77 - 35.73 = 3.04 → j reste à 0

   Tour 2 : i=1, j=0
     amount = min(3.03, 3.04) = 3.03
     Transaction : Bob → Chloe : 3.03€
     debtors[1][1] = 3.03 - 3.03 = 0 → i passe à 2
     creditors[0][1] = 3.04 - 3.03 = 0.01 → j passe à 1

   i=2, j=1 → Boucle terminée (i >= len(debtors))

7. Résultat final :
   transactions = [
     {"from": "Alice", "to": "Chloe", "amount": 35.73},
     {"from": "Bob", "to": "Chloe", "amount": 3.03}
   ]
```

**Sans cet algorithme**, il faudrait 3 transactions (Alice→Chloe, Bob→Chloe, et Chloe rembourse la différence). **Avec l'algorithme glouton**, on minimise le nombre de transactions à **2** (au lieu de 3).

##### Pourquoi cet algorithme est efficace ?

- **Complexité** : O(n log n) pour le tri + O(n) pour le parcours = **O(n log n)** total.
- **Optimalité** : Il minimise le nombre de transactions. C'est un algorithme classique de "minimum cash flow".
- **Démonstration** : Si tous les soldes sont triés (débiteurs décroissants, créanciers décroissants), chaque transaction épuise au moins un participant (le débiteur OU le créancier). Au pire, on a `n-1` transactions pour `n` participants.

---

## 12. expenses/urls.py

**Chemin** : `djancount/expenses/urls.py`
**Rôle** : Définit les routes de l'application `expenses`.

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, ExpenseViewSet, event_detail_view, homepage_view
```

### Configuration du Router DRF

```python
router = DefaultRouter()
router.register(r'events', EventViewSet, basename='event')
router.register(r'expenses', ExpenseViewSet, basename='expense')
```

**`DefaultRouter`** : Routeur DRF qui génère automatiquement les routes REST.

| Appel | Routes générées |
|-------|-----------------|
| `router.register(r'events', EventViewSet, basename='event')` | `/api/events/` (liste + création), `/api/events/{pk}/` (détail + modif + suppression) |
| `router.register(r'expenses', ExpenseViewSet, basename='expense')` | `/api/expenses/` (liste + création), `/api/expenses/{pk}/` (détail + modif + suppression) |

| Paramètre | Rôle |
|-----------|------|
| `r'events'` | Préfixe de l'URL (le `r` indique une raw string) |
| `EventViewSet` | La classe ViewSet associée |
| `basename='event'` | Préfixe pour les noms inversés (`event-list`, `event-detail`) |

**Routes générées automatiquement** :

| URL | Méthode | Nom | Vue |
|-----|---------|-----|-----|
| `/api/events/` | GET | `event-list` | `list` |
| `/api/events/` | POST | `event-list` | `create` |
| `/api/events/{pk}/` | GET | `event-detail` | `retrieve` |
| `/api/events/{pk}/` | PUT | `event-detail` | `update` |
| `/api/events/{pk}/` | PATCH | `event-detail` | `partial_update` |
| `/api/events/{pk}/` | DELETE | `event-detail` | `destroy` |
| (idem pour `/api/expenses/`) | | | |

### Routes classiques

```python
urlpatterns = [
    path('', homepage_view, name='homepage'),
    path('event/<int:event_id>/', event_detail_view, name='event_detail'),
    path('api/', include(router.urls)),
]
```

| Route | Destination | Rôle |
|-------|-------------|------|
| `''` (racine) | `homepage_view` | Page d'accueil avec cartes vers les événements |
| `event/<int:event_id>/` | `event_detail_view` | Vue HTML du bilan financier |
| `api/` | `router.urls` | Toutes les routes API REST |

**`<int:event_id>`** : Paramètre d'URL converti en entier. Django valide que la valeur est un entier et la passe à la vue comme argument.

**`include(router.urls)`** : Inclut toutes les routes générées par le router DRF sous le préfixe `api/`.

---

## 13. expenses/migrations/0001_initial.py

**Chemin** : `djancount/expenses/migrations/0001_initial.py`
**Rôle** : Migration initiale qui crée les tables `Event` et `Expense` dans la base de données.

```python
class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(...)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('participants', models.ManyToManyField(...)),
            ],
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(...)),
                ('title', models.CharField(max_length=200)),
                ('amount', models.DecimalField(...)),
                ('date', models.DateField(auto_now_add=True)),
                ('event', models.ForeignKey(...)),
                ('payer', models.ForeignKey(...)),
            ],
        ),
    ]
```

**Concept Django** : Les migrations sont des fichiers Python qui décrivent les changements de schéma de la base de données.

| Élément | Rôle |
|---------|------|
| `initial = True` | C'est la première migration (aucune dépendance interne) |
| `dependencies` | Dépend du modèle `User` (car les ForeignKey le référencent) |
| `operations` | Liste des opérations SQL à exécuter |
| `CreateModel` | Crée une table avec ses colonnes |

**Commandes associées** :
```bash
python manage.py makemigrations expenses  # Génère ce fichier à partir des modèles
python manage.py migrate                  # Exécute le SQL pour créer les tables
```

**Note** : Ce fichier est **généré automatiquement** par Django. On ne l'édite presque jamais manuellement.

---

## 14. expenses/management/commands/seed.py

**Chemin** : `djancount/expenses/management/commands/seed.py`
**Rôle** : Commande de management Django pour injecter des données de test.

```python
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from expenses.models import Event, Expense
```

**Concept Django** : Les commandes de management sont des scripts exécutables via `python manage.py <nom_commande>`. Elles vivent dans `<app>/management/commands/`.

### Structure obligatoire

```python
class Command(BaseCommand):
    help = "Injecte des donnees de demonstration"

    def handle(self, *args, **kwargs):
        # Le code de la commande ici
```

| Élément | Rôle |
|---------|------|
| `class Command(BaseCommand)` | Classe obligatoire. Le nom DOIT être `Command`. |
| `help` | Description affichée dans `python manage.py help seed` |
| `handle()` | Méthode exécutée quand on lance la commande |

### Contenu de handle()

```python
        Expense.objects.all().delete()
        Event.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()
```
- **Vide les tables** dans l'ordre inverse des dépendances (d'abord les enfants, puis les parents).
- **`is_superuser=False`** : Conserve les superutilisateurs (admins Django). Seules les données de test sont supprimées.
- **Idempotence** : La commande peut être relancée sans crée des doublons.

```python
        alice = User.objects.create_user("alice", email="alice@example.com",
                                         password="password123", first_name="Alice")
```
- **`create_user()`** : Méthode du manager `User`. Crée un utilisateur avec le mot de passe **haché** (pas en clair).
- **Paramètres** : username, email, password, first_name.
- **Retourne** : L'objet `User` créé.

```python
        event1 = Event.objects.create(
            name="Week-end a la mer",
            description="Trois jours a Biarritz",
        )
        event1.participants.set([alice, bob, chloe])
```
- **`Event.objects.create()`** : Crée et sauvegarde un objet `Event` en une seule étape.
- **`event1.participants.set([...])`** : Définit les participants de l'événement. `set()` remplace la liste existante.

```python
        Expense.objects.create(title="Essence", amount=45.50, payer=alice, event=event1)
```
- Crée une dépense liée à Alice et à l'événement `event1`.

### Exécution

```bash
python manage.py seed
```

**Résultat** : 7 utilisateurs, 2 événements, 7 dépenses injectés.

---

## 15. expenses/templates/expenses/event_detail.html

**Chemin** : `djancount/expenses/templates/expenses/event_detail.html`
**Rôle** : Template HTML affichant le bilan financier d'un événement.

### Structure du template

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Bilan de l'Evenement</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 20px auto; padding: 20px; }
        h1, h2 { color: #2c3e50; }
        .summary { background-color: #f1f8ff; padding: 15px; border-radius: 8px; margin-bottom: 20px; }
        .positive { color: green; font-weight: bold; }
        .negative { color: red; font-weight: bold; }
        ul { line-height: 1.6; }
    </style>
</head>
```
- CSS inline (pas de fichier externe) pour un rendu propre.
- `.positive` = vert (créancier), `.negative` = rouge (débiteur).

### Section Résumé

```html
    <div class="summary">
        <h2>Resume</h2>
        <p><strong>Total des depenses :</strong> {{ total }} EUR</p>
        <p><strong>Part theorique par personne :</strong> {{ part }} EUR</p>
    </div>
```

- **`{{ total }}`** : Variable du contexte (le total des dépenses calculé dans la vue).
- **`{{ part }}`** : La part par personne.

**Concept Django Templates** : `{{ variable }}` affiche la valeur de la variable. Appelle `str()` sur l'objet.

### Section Détail des dépenses

```html
    <h2>Detail des depenses</h2>
    <ul>
        {% for expense in expenses %}
            <li><strong>{{ expense.title }}</strong> : {{ expense.amount }} EUR paye par <em>{{ expense.payer }}</em></li>
        {% endfor %}
    </ul>
```

- **`{% for expense in expenses %}`** : Boucle sur la liste des dépenses.
- **`{{ expense.title }}`** : Titre de la dépense.
- **`{{ expense.amount }}`** : Montant.
- **`{{ expense.payer }}`** : Appelle `str(expense.payer)` → retourne le `username` (car `User.__str__` retourne `username`).
- **`{% endfor %}`** : Fin de la boucle.

**Concept Django Templates** : `{% tag %}` pour les instructions (boucles, conditions). `{{ variable }}` pour l'affichage.

### Section Soldes

```html
    <h2>Solde de chaque participant</h2>
    <ul>
        {% for nom, solde in balances.items %}
            <li>
                {{ nom }} :
                {% if solde > 0 %}
                    <span class="positive">+{{ solde }} EUR</span>
                {% elif solde < 0 %}
                    <span class="negative">{{ solde }} EUR</span>
                {% else %}
                    0 EUR
                {% endif %}
            </li>
        {% endfor %}
    </ul>
```

- **`balances.items`** : Itère sur le dictionnaire `balances` (clé = nom, valeur = solde).
- **`{% if solde > 0 %}`** : Si le solde est positif → vert (créancier).
- **`{% elif solde < 0 %}`** : Si négatif → rouge (débiteur).
- **`{% else %}`** : Si nul → gris (équilibré).

### Section Transactions

```html
    <h2>Qui doit combien a qui ?</h2>
    <ul>
        {% for transaction in transactions %}
            <li><strong>{{ transaction.from }}</strong> doit
                <strong>{{ transaction.amount }} EUR</strong>
                a <strong>{{ transaction.to }}</strong></li>
        {% empty %}
            <li>Les comptes sont parfaitement a l'equilibre !</li>
        {% endfor %}
    </ul>
```

- **`{% empty %}`** : Bloc affiché quand la liste `transactions` est vide.
- Affiche : "Alice doit 35.73 EUR a Chloe"

---

## 16. expenses/templates/expenses/home.html

**Chemin** : `djancount/expenses/templates/expenses/home.html`
**Rôle** : Page d'accueil de l'application. Affiche des cartes cliquables vers chaque événement et des liens vers l'API et le Swagger.

### Structure du template

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>DjanCount - Gestion de depenses partagees</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 900px; margin: 40px auto; padding: 20px; background: #f9f9f9; }
        h1 { color: #2c3e50; text-align: center; font-size: 2.2em; margin-bottom: 10px; }
        .subtitle { text-align: center; color: #7f8c8d; margin-bottom: 40px; }
        .cards { display: flex; gap: 20px; justify-content: center; flex-wrap: wrap; }
        .card {
            background: white; border-radius: 12px; padding: 30px 40px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08); text-decoration: none;
            color: inherit; transition: transform 0.2s, box-shadow 0.2s;
            min-width: 280px; text-align: center;
        }
        .card:hover { transform: translateY(-4px); box-shadow: 0 6px 20px rgba(0,0,0,0.12); }
        .card h2 { color: #2c3e50; margin: 0 0 10px 0; }
        .card p { color: #7f8c8d; margin: 0 0 15px 0; }
        .card .btn {
            display: inline-block; background: #2c3e50; color: white;
            padding: 10px 24px; border-radius: 6px; font-weight: bold;
        }
        .links { text-align: center; margin-top: 40px; }
        .links a {
            display: inline-block; margin: 0 10px; color: #3498db;
            text-decoration: none; font-weight: bold;
        }
        .links a:hover { text-decoration: underline; }
        .footer { text-align: center; margin-top: 50px; color: #bdc3c7; font-size: 0.9em; }
    </style>
</head>
```

- CSS inline avec design moderne (cartes avec ombres, hover effect).
- Layout flexbox pour les cartes responsive.

### Section Titre

```html
<body>
    <h1>DjanCount</h1>
    <p class="subtitle">Gestion de depensees partagees - Type Tricount</p>
```

- Titre principal de l'application.
- Sous-titre descriptif.

### Section Cartes événements

```html
    <div class="cards">
        <a class="card" href="/event/1/">
            <h2>Week-end a la mer</h2>
            <p>Alice, Bob, Chloe - 3 participants</p>
            <span class="btn">Voir le bilan</span>
        </a>
        <a class="card" href="/event/2/">
            <h2>Week-end Biarritz Equipe</h2>
            <p>Seer, Julie, Conambot, Remi - 4 participants</p>
            <span class="btn">Voir le bilan</span>
        </a>
    </div>
```

- Chaque carte est un lien `<a>` cliquable vers `/event/{id}/`.
- Contient le nom de l'événement, la liste des participants, et un bouton "Voir le bilan".
- Effet hover : la carte se soulève légèrement (`translateY(-4px)`).

### Section Liens utiles

```html
    <div class="links">
        <a href="/api/events/">API Events</a>
        <a href="/api/expenses/">API Expenses</a>
        <a href="/api/docs/">Swagger UI</a>
        <a href="/admin/">Admin Django</a>
    </div>
```

- Liens rapides vers l'API REST, le Swagger et l'admin Django.
- Utile pour la présentation : accès rapide à toutes les endpoints.

### Footer

```html
    <p class="footer">DjanCount &copy; 2026 - Projet Django REST Framework</p>
</body>
</html>
```

---

## 17. drf-spectacular (Swagger UI)

**Chemin** : Package installé via `pip install drf-spectacular`
**Rôle** : Génère automatiquement la documentation de l'API REST au format OpenAPI 3.0. Affiche une interface Swagger UI interactive.

### Installation

```bash
pip install drf-spectacular
```

### Configuration dans settings.py

```python
INSTALLED_APPS = [
    ...
    'drf_spectacular',
    ...
]

REST_FRAMEWORK = {
    ...
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'DjanCount API',
    'DESCRIPTION': 'API REST de gestion de depensees partagees (type Tricount)',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}
```

| Setting | Rôle |
|---------|------|
| `DEFAULT_SCHEMA_CLASS` | Indique à DRF d'utiliser drf-spectacular pour générer le schéma |
| `TITLE` | Titre affiché dans Swagger UI |
| `DESCRIPTION` | Description de l'API |
| `VERSION` | Version de l'API |
| `SERVE_INCLUDE_SCHEMA` | `False` = ne pas servir le schéma brut via Swagger UI |

### Routes dans config/urls.py

```python
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    ...
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
```

| Route | Rôle |
|-------|------|
| `/api/schema/` | Génère le schéma OpenAPI brut (JSON). Utilisé comme source de données par Swagger UI. |
| `/api/docs/` | Interface Swagger UI interactive. Permet de tester les endpoints directement dans le navigateur. |

### Comment ça marche

1. **drf-spectacular** analyse automatiquement tous les ViewSets et Sérialiseurs du projet.
2. Il génère un schéma OpenAPI 3.0 décrivant chaque endpoint (URL, méthode, paramètres, réponse).
3. **Swagger UI** (`/api/docs/`) lit ce schéma et affiche une interface interactive.
4. Sur la page Swagger, on peut :
   - Voir tous les endpoints (GET, POST, PUT, PATCH, DELETE)
   - Lire la description de chaque endpoint
   - Tester les requêtes directement (bouton "Try it out")
   - Voir les schémas des objets (Event, Expense)

### Avantages pour la présentation

- **Documentation auto-générée** : Pas besoin de rédiger la doc manuellement.
- **Interactive** : On peut tester l'API en direct pendant la présentation.
- **Professionnel** : L'interface Swagger est un standard dans l'industrie.
- **À jour** : La doc se met à jour automatiquement quand on modifie les ViewSets.

---

## 18. requirements.txt

**Chemin** : `requirements.txt`
**Rôle** : Liste toutes les dépendances Python du projet.

```
Django>=5.2,<5.3
djangorestframework>=3.16,<4
django-debug-toolbar>=6.0,<8
jupyterlab>=4.2,<5
djangorestframework-simplejwt>=5.3,<6.0
django-cors-headers>=4.3,<5.0
gunicorn
whitenoise
drf-spectacular
```

| Package | Version | Rôle |
|---------|---------|------|
| `Django` | >=5.2,<5.3 | Framework web principal |
| `djangorestframework` | >=3.16,<4 | API REST (sérialiseurs, viewsets, router) |
| `django-debug-toolbar` | >=6.0,<8 | Barre de debug (requêtes SQL, performance) |
| `jupyterlab` | >=4.2,<5 | Notebook Jupyter (développement/data) |
| `djangorestframework-simplejwt` | >=5.3,<6.0 | Authentification JWT (tokens) |
| `django-cors-headers` | >=4.3,<5.0 | Gestion CORS (requêtes cross-origin) |
| `gunicorn` | Dernière | Serveur WSGI de production |
| `whitenoise` | Dernière | Sert les fichiers statiques en production |
| `drf-spectacular` | Dernière | Génération de documentation Swagger/OpenAPI |

**Notation de version** :
- **`>=5.2,<5.3`** : Version 5.2.x uniquement (pas de 5.3+). Protège contre les breaking changes.
- **`>=3.16,<4`** : Version 3.16.x ou supérieure, mais pas 4.0+.

**Installation** :
```bash
pip install -r requirements.txt
```

---

## 19. Algorithme du bilan financier — Ligne par ligne

> Cette section reprend l'algo de la section 11 avec encore plus de détails.

### Contexte

Quand un groupe partage des dépenses, certains ont payé plus que leur part, d'autres moins. L'algorithme calcule le **minimum de transactions** nécessaires pour équilibrer les comptes.

### Données d'entrée

```python
expenses = [
    {"title": "Essence",    "amount": 45.50,  "payer": "Alice"},
    {"title": "Courses",    "amount": 78.20,  "payer": "Bob"},
    {"title": "Restaurant", "amount": 120.00, "payer": "Chloe"},
]
participants = ["Alice", "Bob", "Chloe"]
```

### Étape 1 : Total et part théorique

```python
total_expenses = sum(expense.amount for expense in expenses)
# total_expenses = 45.50 + 78.20 + 120.00 = 243.70
```

```python
part_per_person = total_expenses / len(participants)
# part_per_person = 243.70 / 3 = 81.23333... → 81.23 (arrondi flottant)
```

**Concept** : La "part théorique" est ce que chaque personne devrait payer si les dépenses étaient réparties équitablement.

### Étape 2 : Initialisation des soldes

```python
balances = {
    "Alice": -81.23,  # Alice "doit" 81.23€
    "Bob": -81.23,    # Bob "doit" 81.23€
    "Chloe": -81.23   # Chloe "doit" 81.23€
}
```

**Pourquoi négatif ?** : On modélise la dette initiale. Chaque personne part avec une dette égale à sa part. C'est un point de départ neutre.

### Étape 3 : Mise à jour avec les paiements réels

```python
# Alice a payé 45.50€
balances["Alice"] = -81.23 + 45.50 = -35.73

# Bob a payé 78.20€
balances["Bob"] = -81.23 + 78.20 = -3.03

# Chloe a payé 120.00€
balances["Chloe"] = -81.23 + 120.00 = +38.77
```

**Interprétation des soldes** :

| Personne | Solde | Signification |
|----------|-------|---------------|
| Alice | -35.73 | Elle a payé 35.73€ de **moins** que sa part |
| Bob | -3.03 | Il a payé 3.03€ de **moins** que sa part |
| Chloe | +38.77 | Elle a payé 38.77€ de **plus** que sa part |

**Vérification** : `-35.73 + (-3.03) + 38.77 = 0.01` (erreur d'arrondi du flottant).

### Étape 4 : Classification

```python
debtors = [
    ["Alice", 35.73],   # Alice doit 35.73€
    ["Bob", 3.03]        # Bob doit 3.03€
]

creditors = [
    ["Chloe", 38.77]     # On doit 38.77€ à Chloe
]
```

**Seuil de 0.01** : Les soldes entre -0.01 et +0.01 sont considérés comme nuls (erreurs d'arrondi).

### Étape 5 : Algorithme glouton

**Principe** : On parcourt les débiteurs et créanciers en parallèle. À chaque étape, on transfère le maximum possible entre le débiteur courant et le créancier courant.

**Tour 1** :
```
i=0 (Alice, 35.73€), j=0 (Chloe, 38.77€)
amount = min(35.73, 38.77) = 35.73

Transaction : Alice → Chloe : 35.73€

Mise à jour :
  Alice : 35.73 - 35.73 = 0 → i passe à 1 (Alice est réglée)
  Chloe : 38.77 - 35.73 = 3.04 → j reste à 0 (Chloe attend encore)
```

**Tour 2** :
```
i=1 (Bob, 3.03€), j=0 (Chloe, 3.04€)
amount = min(3.03, 3.04) = 3.03

Transaction : Bob → Chloe : 3.03€

Mise à jour :
  Bob : 3.03 - 3.03 = 0 → i passe à 2 (Bob est réglé)
  Chloe : 3.04 - 3.03 = 0.01 → j passe à 1 (Chloe est considérée réglée, seuil 0.01)
```

**Fin** : `i=2 >= len(debtors)=2` → Boucle terminée.

### Résultat final

```python
transactions = [
    {"from": "Alice", "to": "Chloe", "amount": 35.73},
    {"from": "Bob", "to": "Chloe", "amount": 3.03}
]
```

**Seulement 2 transactions** au lieu de 3 possibles (sans optimisation).

### Visualisation

```
AVANT :
  Alice   : -35.73€ (doit)
  Bob     :  -3.03€ (doit)
  Chloe   : +38.77€ (est créancière)

APRÈS les transactions :
  Alice   : 0€ (a remboursé Chloe)
  Bob     : 0€ (a remboursé Chloe)
  Chloe   : +38.77 - 35.73 - 3.03 = +0.01€ ≈ 0€
```

### Pourquoi cet algorithme est-il optimal ?

1. **Nombre minimum de transactions** : Chaque transaction épuise au moins un participant (le débiteur OU le créancier). Au pire, on a `n-1` transactions pour `n` participants.

2. **Complexité temporelle** : O(n log n) pour le tri (si on triait les listes) + O(n) pour le parcours = O(n log n) total.

3. **Complexité spatiale** : O(n) pour stocker les débiteurs et créanciers.

4. **Correction** : La somme des soldes est toujours ≈ 0 (à l'erreur d'arrondi près). Toutes les dettes sont honorées.

### Cas limites

| Cas | Comportement |
|-----|--------------|
| Tous les soldes = 0 | Aucune transaction (liste vide) |
| 1 seul débiteur, 1 seul créancier | 1 seule transaction |
| Débiteur = créancier (montants égaux) | Les deux `if` sont vrais, `i` et `j` avancent |
| Montants très proches (arrondi) | Seuil de 0.01 évite les micro-transactions |
| Pas de participants | `part_per_person = 0`, tous les soldes = 0 |

---

*Document généré pour le projet DjanCount — Explications complètes de l'architecture Django.*
