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


## Test


pytest app/tests -vvs

pytest app/tests -ra -vvs --cov=app 


pytest app/tests -ra -vvs --cov=app --cov-branch --cov-report=term-missing --cov-report=html


pytest --cov=app/src --cov-report=term-missing


pytest app/tests/presentation/test_tag_route.py


ptw . -vvs

pytest -vv --cov=app/src --cov-branch --cov-report=term-missing --cov-report=html


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


