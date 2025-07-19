# H₂Optimize - Backend

## Avant de lancer

**S’assurer que la base de données est lancée**
Le backend dépend du réseau `postgres_net` qui est créé automatiquement lors du lancement du service Postgres.

## Lancer l’application

```bash
make startd
```

**Autres commandes utiles**

```bash
make help
```

## Nettoyer le code

Linter + Formateur : **ruff**
Le linter ne corrige pas automatiquement les erreurs qu’il détecte.

```bash
make lint

>>> docker compose exec backend sh -c "ruff check /code/app/src/"
>>> All checks passed!
```

Extension VS Code :

[Ruff extension for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff)

## Gestion des migrations

* [Documentation Alembic](https://alembic.sqlalchemy.org/en/latest/index.html#)
* [Documentation espace Confluence](https://j-renevier.atlassian.net/wiki/x/AgDXCw)

## Tests

[Documentation pytest](https://docs.pytest.org/en/stable/reference/reference.html)

## Ajout des dépendances

Lors de l’ajout d’une dépendance en développement :

* L’installer dans le conteneur.
* L’ajouter dans `app/pyproject.toml`

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

Le fichier `requirements.txt` est présent uniquement à titre indicatif, il **n’est jamais utilisé** dans les environnements.

La commande `make pipinstall` :

```bash
docker compose exec backend sh -c "pip install $(LIB) && pip freeze > /code/app/requirements.txt"
```

Permet seulement d’installer la dépendance dans le conteneur et de mettre à jour le `requirements.txt`, mais ce n’est **pas suffisant** pour gérer proprement les dépendances du projet.


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

Configurer app/src/infrastructure/migrations/env.py pour qu’il puisse générer automatiquement les migrations

```py
# app/src/infrastructure/migrations/env.py
# Importer les models
from app.src.infrastructure.db.models.tag_model import TagModel
# Cibler les metadata
target_metadata = SQLModel.metadata
```

Générer automatiquement un fichier de migration a partir de SQLModel

```
root@708b091e98e1:/code/app # alembic revision --autogenerate -m'test'
>>> INFO  [alembic.autogenerate.compare] Detected type change from TIMESTAMP(timezone=True) to DateTime() on 'tag.updated_at'
>>> Generating
>>> /code/app/src/infrastructure/migrations/versions/30ccca2a5199_test.py ...  done
```


## Tests

**Executer tout les tests**

```bash
pytest app/tests -vvs
```

**Executer les tests d'intégration**

```bash
pytest app/tests/integration -vvs
```

**Executer les tests unitaire**

```bash
pytest app/tests/unit -vvs
```

### Couverture

**Executer tout les tests avec la couverture**

```bash
pytest app/tests -vvs --cov=app 
```

**Executer tout les tests avec la couverture et le rapport**

```bash
pytest app/tests -vvs --cov=app --cov-report=html
```

### Watch mode

Remplacer `pytest` par `ptw`

Disclaimer : pytest-watcher est aussi observateur que Daredevil

---



Lancement du projet sans docker 

dans bash 


python3 -m venv venv

source venv/Scripts/activate

python -m pip install --upgrade pip

pip install "fastapi[standard]"

https://github.com/fastapi/full-stack-fastapi-template/blob/master/backend/app/api/routes/utils.py

https://github.com/faraday-academy/fast-api-lms/blob/7-async-and-code-cleanup/api/users.py


middleware 
sql 
dependencies 


ref 
https://github.com/zhanymkanov/fastapi-best-practices


https://github.com/fastapi/full-stack-fastapi-template/tree/master/backend
https://github.com/faraday-academy/fast-api-lms/tree/7-async-and-code-cleanup
https://github.com/codingforentrepreneurs/analytics-api/tree/main


