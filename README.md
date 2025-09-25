# H₂Optimize - Backend

![archi](./doc/images/archi.png)

---

## Organisation du code

```
BACKEND/
├── app/                               # Code source de l'application
│   ├── src/                          
│   │   ├── common/                    # Helpers et utilitaires
│   │   │
│   │   ├── domain/                    # Couche métier
│   │   │   ├── entities/              # Modèles métier
│   │   │   ├── interface_repositories/# Abstraction des repositories : interface entre le métier et la persistance
│   │   │
│   │   ├── infrastructure/            # Couches externes : persistance des données
│   │   │   ├── db/                    
│   │   │   │   ├── models/            # Modèles ORM SQLAlchemy
│   │   │   │   ├── repositories/      # Implémentations des repositories
│   │   │   │   │   └── tag_repository_sql.py
│   │   │   │   └── session.py         # Gestion des sessions DB
│   │   │   ├── migrations/            # Migrations et utilitaires pour les appliquer        
│   │   │   │   ├── versions/          # Versions de la DB
│   │   │   │   │   └── f743ab8a8305_start.py # Version spécifique de la DB
│   │   │
│   │   ├── presentation/              # Couche de présentation
│   │   │   ├── api/                   # Implémentation des API
│   │   │   │   ├── common/            # Helpers et utilitaires pour les API
│   │   │   │   ├── tag/               # Routes spécifiques
│   │   │   │   │   ├── tag_model.py   # Modèles des données d’entrée et de sortie des endpoints
│   │   │   │   │   ├── tag_route.py   # Endpoints API Tag
│   │   │   ├── router.py              # Assemblage des routes API
│   │   │   ├── static/                # Rendu des fichiers statiques
│   │   │   ├── dependencies.py        # Gestion des dépendances
│   │   │   ├── core/                  # Configuration FastAPI
│   │   │   └── main.py                # Point d’entrée FastAPI
│   │   │
│   │   ├── use_cases/                 # Cas d’usage (besoins métier)
│   │   │   └── tag/                   # Cas d’usage spécifiques
│   │   │       ├── create_tag_use_case.py
│   │   │       ├── delete_tag_use_case.py
│   │   │       ├── get_tag_by_id_use_case.py
│   │   │       ├── get_tags_list_use_case.py
│   │   │       ├── update_tag_use_case.py
│   ├── alembic.ini                    # Configuration des migrations
│   └── pyproject.toml                 # Métadonnées et config du projet
│
├── tests/                             # Tests automatisés
│   ├── integration/                   # Tests d’intégration (API + DB)
│   ├── unit/                          # Tests unitaires (isolés à 100 %)
│   └── conftest.py                    # Utilitaires partagés pour les tests d’intégration et unitaires
│
├── migrations/                        # Scripts Alembic pour la DB (migrations)
├── logs/                              # Logs (si configurés)
├── doc/                               # Documentation backend
├── docker-compose.yml                 # Orchestration des services Docker
├── Dockerfile                         # Image Docker
├── Makefile                           # Commandes
└── README.md
```

---

## Avant de lancer

**S’assurer que la base de données est lancée**
Le backend dépend du réseau `postgres_net`, qui est créé automatiquement lors du lancement du service Postgres.

---

## Lancer l’application

```bash
make startd
```

---

### Autres commandes utiles

```bash
make help
```

---

## Nettoyer le code

Linter + formateur : **ruff**
Le linter ne corrige pas automatiquement les erreurs qu’il détecte.

```bash
make lint

>>> docker compose exec backend sh -c "ruff check /code/app/src/"
>>> All checks passed!
```

Extension VS Code recommandée :
[Ruff extension for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff)

---

## Gestion des migrations

* [Documentation Alembic](https://alembic.sqlalchemy.org/en/latest/index.html#)
* [Documentation interne Confluence](https://j-renevier.atlassian.net/wiki/x/AgDXCw)

---

## Tests

* [Documentation pytest](https://docs.pytest.org/en/stable/reference/reference.html)

---

## Ajout de dépendances

Lors de l’ajout d’une dépendance en développement :

1. L’installer dans le conteneur.
2. L’ajouter dans `app/pyproject.toml`.

En fonction du type de dépendance, l’ajouter au bon endroit :

```toml
[project]
name = "H2Optimize"
...
dependencies = [
    "alembic",
    "email_validator",
    ..., 
    # Autres dépendances nécessaires en production
]

[project.optional-dependencies]
dev = [
    "pytest",
    "pytest-asyncio",
    ..., 
    # Autres dépendances nécessaires en développement
]
```

**Remarque :** Le fichier `requirements.txt` est uniquement **indicatif** et **n’est jamais utilisé** dans les environnements.

La commande `make pipinstall` :

```bash
docker compose exec backend sh -c "pip install $(LIB) && pip freeze > /code/app/requirements.txt"
```

Installe une dépendance dans le conteneur et met à jour le `requirements.txt`, mais ce n’est **pas suffisant** pour gérer proprement les dépendances du projet.

![alt text](./doc/images/pyproject.png)

---

## Migrations

### Configuration

```ini
[alembic]

script_location = %(here)s/src/infrastructure/migrations
prepend_sys_path = %(here)s/../.
path_separator = os
sqlalchemy.url = postgresql://admin:Changeme!1@postgres/app

...
```

Configurer `app/src/infrastructure/migrations/env.py` pour qu’il puisse générer automatiquement les migrations :

```py
# app/src/infrastructure/migrations/env.py
# Importer les modèles
from app.src.infrastructure.db.models.tag_model import TagModel
# Cibler les metadata
target_metadata = SQLModel.metadata
```

Générer automatiquement un fichier de migration à partir de SQLModel :

```bash
root@708b091e98e1:/code/app # alembic revision --autogenerate -m 'test'
>>> INFO  [alembic.autogenerate.compare] Detected type change from TIMESTAMP(timezone=True) to DateTime() on 'tag.updated_at'
>>> Generating
>>> /code/app/src/infrastructure/migrations/versions/30ccca2a5199_test.py ...  done
```

---

## Tests

### Commandes Make 

`make test` => run tout les tests avec la couverture 

`make coverage` => run tout les tests avec la couverture et génére le rapport

⚠️ Le container doit être en marche pour que les tests puissent s'éxécuter


### Lancer tous les tests

```bash
ENVIRONMENT=testing pytest app/tests -vvs
```

### Lancer uniquement les tests d’intégration

```bash
ENVIRONMENT=testing pytest app/tests/integration -vvs
```

### Lancer uniquement les tests unitaires

```bash
ENVIRONMENT=testing pytest app/tests/unit -vvs
```

---

### Couverture

**Exécuter tous les tests avec la couverture :**

```bash
ENVIRONMENT=testing pytest app/tests -vvs --cov=app 
```

**Exécuter tous les tests avec la couverture + rapport HTML :**

```bash
ENVIRONMENT=testing pytest app/tests -vvs --cov=app --cov-report=html
```

---

### Watch mode

Remplacer `pytest` par `ptw`.

*Disclaimer : pytest-watcher est aussi observateur que Daredevil*


### Env

#### En local

Ce baser sur le fichier .env & .env.template

#### CI / CD

Ce baser sur le fichier .env.action.template

### ⚠️ Troubleshooting – Erreur `/entrypoint.sh: not found` dans le conteneur *watcher* sous Windows

**Erreur :**

```
/bin/sh: /entrypoint.sh: not found
```

**Origine :**

> Incompatibilité des **séquences de fin de ligne** entre Windows et Linux.

Les systèmes utilisent des conventions différentes pour terminer les lignes dans les fichiers texte :

| Système         | Séquence de fin de ligne | Représentation |
| --------------- | ------------------------ | -------------- |
| **Windows**     | `CRLF`                   | `\r\n`         |
| **Linux/macOS** | `LF`                     | `\n`           |

**Solution :**
Convertir le fichier en `LF` avec VSCode :

![Fin de ligne VSCode](./doc/image/sequence_end_line.png)


### Référence

- https://github.com/zhanymkanov/fastapi-best-practices
- https://github.com/fastapi/full-stack-fastapi-template/tree/master/backend
- https://github.com/faraday-academy/fast-api-lms/tree/7-async-and-code-cleanup
- https://github.com/codingforentrepreneurs/analytics-api/tree/main
