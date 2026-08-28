# Rapport individuel — Sécurité JWT et permissions

**Branche :** `feature/jwt-security`  
**Périmètre :** authentification JWT et contrôle d’accès de l’API REST DjanCount

## Objectif

Sécuriser l’API REST avec des tokens JWT et limiter l’accès aux événements et aux dépenses liés à l’utilisateur connecté.

## Dépendances installées

Les dépendances suivantes ont été ajoutées dans `requirements.txt` :

```text
djangorestframework-simplejwt>=5.3,<6.0
django-cors-headers>=4.3,<5.0
```

## Configuration DRF

Dans `djancount/config/settings.py` :

- `JWTAuthentication` est configurée comme classe d’authentification par défaut ;
- `IsAuthenticatedOrReadOnly` reste la permission globale de référence ;
- les durées JWT sont configurées avec une durée de vie d’une heure pour l’access token et d’un jour pour le refresh token.

Les ViewSets appliquent ensuite des permissions métier plus strictes, détaillées ci-dessous.

## Routes d’authentification

Dans `djancount/config/urls.py`, deux endpoints sont disponibles :

| Méthode | Endpoint | Fonction |
|---|---|---|
| POST | `/api/token/` | Vérifie les identifiants et retourne un access token et un refresh token |
| POST | `/api/token/refresh/` | Génère un nouvel access token à partir du refresh token |

Exemple d’obtention d’un token :

```http
POST http://localhost:8000/api/token/
Content-Type: application/json

{
  "username": "<utilisateur>",
  "password": "<mot-de-passe>"
}
```

Pour les requêtes protégées, transmettre uniquement l’access token :

```http
Authorization: Bearer <access_token>
```

## Permissions métier

Le fichier `djancount/expenses/permissions.py` contient deux permissions :

### `IsEventParticipant`

- l’utilisateur doit être authentifié ;
- un événement n’est accessible qu’à ses participants ;
- un administrateur (`is_staff`) conserve un accès complet.

### `IsPayerOrEventParticipant`

- l’utilisateur doit être authentifié ;
- une dépense est accessible à son payeur ou aux participants de l’événement associé ;
- un administrateur conserve un accès complet.

Les permissions sont déclarées explicitement dans `EventViewSet` et `ExpenseViewSet`.

### Pourquoi des permissions métier personnalisées ?

`IsAuthenticatedOrReadOnly` répond uniquement à une règle générale : autoriser la lecture aux utilisateurs anonymes et réserver les écritures aux utilisateurs authentifiés. Elle ne sait pas déterminer si un utilisateur participe à un événement ou s’il est lié à une dépense.

Les permissions personnalisées ajoutent donc la règle fonctionnelle propre à DjanCount : l’accès dépend des relations entre `User`, `Event` et `Expense`. Elles complètent l’authentification JWT et permettent de centraliser ces contrôles dans un composant réutilisable et testable.

## Filtrage des listes

Les méthodes `get_queryset()` de `djancount/expenses/views.py` filtrent les résultats des endpoints de liste :

- `/api/events/` ne retourne que les événements auxquels l’utilisateur participe ;
- `/api/expenses/` ne retourne que les dépenses qu’il a payées ou liées à ses événements ;
- les administrateurs voient toutes les ressources.

Ce filtrage est nécessaire car une permission objet seule ne suffit pas pour sécuriser un endpoint de liste.

## Scénarios possibles

Les requêtes HTTP sont documentées dans `http-requests/jwt.http`, `http-requests/events.http` et `http-requests/expenses.http`.

Scénarios à vérifier :

1. obtenir les tokens avec `/api/token/` ;
2. renouveler l’access token avec `/api/token/refresh/` ;
3. appeler une ressource avec `Authorization: Bearer <access_token>` ;
4. vérifier qu’un utilisateur ne voit pas les événements ou dépenses qui ne lui sont pas liés ;
5. vérifier qu’une requête sans token reçoit `401 Unauthorized` ;
6. vérifier qu’un utilisateur non participant reçoit `403 Forbidden` sur une ressource existante ;
7. vérifier qu’un administrateur peut accéder à toutes les ressources.

Les identifiants, tokens et refresh tokens utilisés pour les tests doivent rester locaux et ne pas être commités dans le dépôt.

## Validation

La commande suivante ne signale aucune erreur Django :

```bash
python djancount/manage.py check
```

Résultat attendu :

```text
System check identified no issues (0 silenced).
```
