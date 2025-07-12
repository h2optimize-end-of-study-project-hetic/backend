#!/bin/bash
set -e

alembic -c /code/app/src/alembic.ini upgrade head

echo "Migrations terminées. Lancement de l'application"

exec "$@"