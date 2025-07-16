# H₂Optimize - Backend

## Avant de lancer 

**S'assurer que la base de donné est lancé** 
Le back depend du reseau postgres_net qui est construit automatiqument en lançant postgres

## Lancer l'application 

```bash
make startd
```

**Plus de commande utiles** 
```bash
make help 
```

## Clean le code

Linter + Formater : ruff 
Le linter ne fix pas automatiquement les erreurs qu'il remonte

```bash
make lint

>>> docker compose exec backend sh -c "ruff check /code/app/src/"
>>> All checks passed!
```

Extension VS Code 

[Ruff extension for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff)




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