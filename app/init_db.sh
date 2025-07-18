#!/bin/bash
set -e

alembic -c /code/app/alembic.ini upgrade head

alembic -c /code/app/alembic.ini history

echo "Migrations terminées. Lancement de l'application"

exec "$@"