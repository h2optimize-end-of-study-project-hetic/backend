# H₂Optimize - Backend

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



Alembic 

pip install alembic



root@708b091e98e1:/code/app/src# alembic init infrastructure/migrations

Fichier `alembic.ini` autogénéré dans `/code/app/src/alembic.ini`
Dossier `migrations` autogénéré dans `/code/app/src/infrastructure/migrations`

alembic.ini
```ini
sqlalchemy.url = postgresql://admin:Changeme!1@postgres/app
```

Creer un fichier de migration 
`root@708b091e98e1:/code/app/src# alembic revision -m 'first migration'`

```py
"""first migration

Revision ID: f7b3f1860b4a
Revises: 
Create Date: 2025-07-12 06:00:48.847893

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f7b3f1860b4a'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "employee",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.column("name", sa.String(50), nullable=False),
        sa.column("current", sa.Boolean,  default=True)
    )

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("employee")
```

Migrer le dernier fichier

``` sh 
root@708b091e98e1:/code/app/src# alembic upgrade head
>>>INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
>>>INFO  [alembic.runtime.migration] Will assume transactional DDL.
>>>INFO  [alembic.runtime.migration] Running upgrade  -> f7b3f1860b4a, first migration
```

```sh
root@708b091e98e1:/code/app/src# alembic history
>>><base> -> f7b3f1860b4a (head), first migration
```

```sh 
root@708b091e98e1:/code/app/src# alembic current
>>>INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
>>>INFO  [alembic.runtime.migration] Will assume transactional DDL.
>>>f7b3f1860b4a (head)
``` 

```sh
root@708b091e98e1:/code/app/src# alembic downgrade -1
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running downgrade f7b3f1860b4a -> , first migration
```

import from infrastructure.db.models.tag_model import TagModel dan env;py
target_metadata = SQLModel.metadata

root@708b091e98e1:/code/app/src# alembic revision --autogenerate -m'test'

INFO  [alembic.autogenerate.compare] Detected type change from TIMESTAMP(timezone=True) to DateTime() on 'tag.updated_at'
  Generating
  /code/app/src/infrastructure/migrations/versions/30ccca2a5199_test.py ...  done


ref 
https://github.com/fastapi/full-stack-fastapi-template/tree/master/backend
https://github.com/faraday-academy/fast-api-lms/tree/7-async-and-code-cleanup