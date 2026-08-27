# 🚀 Organisation du Projet - DjanCount (Équipe de 4)

**Application Web & API REST de gestion de dépenses partagées (type Tricount)**  
*Journée de développement : 10h00 - 17h00 (Pause 13h00 - 14h00)*

---

## 📌 1. Objectifs & Exigences du Projet
- **Stack technique** : Python, Django, Django REST Framework (DRF), SimpleJWT, Templates HTML.
- **Règles impératives** :
  1. Tous les membres de l'équipe doivent écrire du code Django.
  2. Aucun blocage entre membres : architecture 100% parallélisée.
  3. Chaque membre tient un **rapport individuel de contribution** (support de notation de TD).
  4. **Relecture croisée obligatoire** : tout le monde doit être capable d'expliquer n'importe quelle partie du projet lors de la soutenance.

---

## 🗂️ 2. Schéma de Données de Base (A valider ensemble de 10h00 à 10h15)

Le projet tourne autour de deux modèles reliés au modèle `User` natif de Django :

### Modèle 1 : `Event` (Événement)
- `name` : `CharField` (ex: "Week-end à la mer")
- `description` : `TextField`
- `participants` : `ManyToManyField` vers `django.contrib.auth.models.User`

### Modèle 2 : `Expense` (Dépense)
- `title` : `CharField` (ex: "Courses", "Essence")
- `amount` : `DecimalField` (montant de la dépense)
- `payer` : `ForeignKey` vers `User` (celui qui a payé)
- `event` : `ForeignKey` vers `Event` (l'événement concerné)
- `date` : `DateField` (auto_now_add=True)

---

## 👥 3. Répartition des Rôles & Responsabilités (Zéro Blocage)

Chaque membre travaille sur sa branche Git et son propre domaine Django sans attendre les autres.

```
                    ┌─────────────────────────────────────────┐
                    │      Squelette Commun (10h-10h15)       │
                    │   models.py + projet Django partagé     │
                    └───────────────────┬─────────────────────┘
                                        │
         ┌──────────────────┬───────────┴───────────┬──────────────────┐
         ▼                  ▼                       ▼                  ▼
┌─────────────────┐ ┌───────────────┐     ┌──────────────────┐ ┌─────────────────┐
│    MEMBRE 1     │ │   MEMBRE 2    │     │     MEMBRE 3     │ │    MEMBRE 4     │
│ Modèles / Admin │ │ API REST DRF  │     │ Security & JWT   │ │ Vue HTML &      │
│ & Data Seed     │ │ Serializers   │     │ Permissions      │ │ Algorithme      │
└─────────────────┘ └───────────────┘     └──────────────────┘ └─────────────────┘
```

### 👨‍💻 Membre 1 : Core Django, Modèles, Admin & Fixtures
* **Branche Git** : `feature/models-admin`
* **Fichiers clés** : `expenses/models.py`, `expenses/admin.py`, `seed.py` (ou `fixtures.json`)
* **Missions** :
  - Écrire et consolider les modèles `Event` et `Expense` (méthodes `__str__`, verbose_name, etc.).
  - Configurer l'admin Django (`admin.py`) avec filtres, recherche et affichage des colonnes pour les 2 modèles.
  - Créer un script `seed.py` / fixture pour injecter des utilisateurs, événements et dépenses de démonstration.
* **Ingrédients du rapport individuel** : Modélisation des données ORM Django, relations ForeignKey/ManyToManyField, configuration de l'Admin Django.

### 👨‍💻 Membre 2 : API REST (DRF), Sérialiseurs & Validation Métier
* **Branche Git** : `feature/api-serializers`
* **Fichiers clés** : `expenses/serializers.py`, `expenses/views.py` (ViewSets), `djancount/urls.py`
* **Missions** :
  - Écrire `EventSerializer` et `ExpenseSerializer`.
  - Implémenter les validations métiers obligatoires :
    - `validate_amount` : vérifier que `amount > 0` (lancer `serializers.ValidationError` si <= 0).
    - `validate` : vérifier que le `payer` fait bien partie des `participants` de l'événement.
  - Créer `EventViewSet` (lecture/création) et `ExpenseViewSet` (CRUD complet) et les enregistrer dans un `DefaultRouter`.
* **Ingrédients du rapport individuel** : Django REST Framework, sérialisation des données, règles de validation métier.

### 👨‍💻 Membre 3 : Authentification JWT & Permissions DRF
* **Branche Git** : `feature/jwt-security`
* **Fichiers clés** : `djancount/settings.py`, `djancount/urls.py`, `expenses/permissions.py`
* **Missions** :
  - Installer et intégrer `djangorestframework-simplejwt`.
  - Configurer les routes d'authentification JWT `/api/token/` et `/api/token/refresh/`.
  - Configurer la permission `IsAuthenticatedOrReadOnly` sur les ViewSets (lecture libre en GET, écriture réservée aux utilisateurs authentifiés avec Token Bearer).
  - Préparer et documenter les requêtes de test Postman / HTTP client pour l'équipe.
* **Ingrédients du rapport individuel** : Authentification stateless JWT, middleware/sécurité Django, système de permissions DRF.

### 👨‍💻 Membre 4 : Vue HTML, Template & Algorithme du Bilan Financier
* **Branche Git** : `feature/html-bilan`
* **Fichiers clés** : `expenses/views.py` (vue classique), `expenses/templates/expenses/event_detail.html`
* **Missions** :
  - Écrire la vue classique Django (`event_detail_view`).
  - Développer l'algorithme Python du **Bilan Financier** dans la vue :
    1. Calculer le total des dépenses de l'événement.
    2. Calculer la part théorique de chaque participant (`Total / nb_participants`).
    3. Calculer le solde net de chaque participant (`Payé - Part_Théorique`).
    4. Identifier qui doit de l'argent (solde négatif) et à qui on en doit (solde positif).
  - Créer le template HTML `event_detail.html` affichant l'événement, ses dépenses et le bilan clair.
* **Ingrédients du rapport individuel** : Vues Django basées sur des fonctions/classes, système de templates Jinja/Django, algorithmique métier en Python.

---

## ⏰ 4. Planning Détaillé de la Journée

| Horaire | Étape | Action collective / individuelle |
|---|---|---|
| **10h00 - 10h15** | 🚀 **Kick-off & Squelette** | Création du projet Django + écriture du `models.py` initial. Tout le monde fait `git pull`. |
| **10h15 - 12h30** | 💻 **Développement Parallèle** | Chacun développe sur sa branche sans dépendance. Membre 1 push son admin vers 11h. |
| **12h30 - 13h00** | 🔀 **Merge v1 & Validation** | Fusion des 4 branches sur `main`. Premier test de bout en bout de l'application. |
| **13h00 - 14h00** | 🍱 **Pause Déjeuner** | Repas. |
| **14h00 - 15h00** | 🧪 **Tests & README** | Rédaction complète du `README.md` (setup venv, migrations, superuser, runserver). Peaufinage des réponses API et du style HTML. |
| **15h00 - 16h15** | 🔄 **Relecture Croisée (Peer-Review)** | **Important** : Chaque membre présente son code aux 3 autres. Tout le monde s'entraîne à réexpliquer le code d'un collègue pour la soutenance. |
| **16h15 - 17h00** | 📄 **Rapports & ZIP** | Rédaction et mise au propre des 4 rapports individuels + création du `.zip` du projet pour le dépôt Teams. |

---

## 🌿 5. Workflow Git de l'Équipe

```bash
# 1. Récupérer le projet
git pull origin main

# 2. Créer et basculer sur sa branche personnelle
git checkout -b feature/<nom-de-votre-feature>

# 3. Travailler et commiter régulièrement
git add .
git commit -m "feat: description claire de ce qui a été fait"

# 4. Envoyer sa branche sur GitHub
git push origin feature/<nom-de-votre-feature>
```

---

## 📝 6. Modèle de Rapport Individuel (A remplir au fil de la journée)

Chaque membre doit rendre un rapport individuel. Voici la structure type à suivre :

```markdown
# Rapport Individuel de Contribution - Projet DjanCount

**Nom & Prénom :** [Votre Nom]
**Date :** [Date du jour]
**Module attribué :** [Ex: API REST, Sérialiseurs & Validation Métier]

---

### 1. Description du travail réalisé
Explication synthétique de vos missions et des fichiers développés.

### 2. Implémentation technique et extraits de code (Snippets)
Insérer des extraits de code Django significatifs que vous avez écrits et les expliquer :
- Pourquoi avoir choisi cette méthode / cette classe ?
- Comment la validation ou la logique fonctionne-t-elle ?

### 3. Difficultés rencontrées et solutions
Description des erreurs rencontrées (ex: erreurs de migration, problème d'importation, permissions JWT) et des solutions trouvées.

### 4. Compréhension de l'application globale
Démontrer votre compréhension globale du projet (expliquez en 5-10 lignes le rôle des 3 autres parties développées par vos camarades).
```
