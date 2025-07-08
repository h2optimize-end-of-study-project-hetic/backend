ENV_FILE=.env
ENV_LOCAL_FILE=.env.local

.PHONY: help build run stop logs start 

start :
	docker compose --env-file $(ENV_FILE) --env-file $(ENV_LOCAL_FILE) up

logs : 
	docker compose logs -f

build: 
	docker compose --env-file $(ENV_FILE) --env-file $(ENV_LOCAL_FILE) up --build

buildd: 
	docker compose --env-file $(ENV_FILE) --env-file $(ENV_LOCAL_FILE) up --build -d

clean: 
	docker compose down

cleanall: 
	docker compose -v down

startd :
	$(MAKE) buildd
	$(MAKE) logs

restartd:
	$(MAKE) clean
	$(MAKE) buildd
	$(MAKE) logs
