ifneq ("$(wildcard .env)","")
	include .env
	export $(shell sed 's/=.*//' .env)
endif

ifneq ("$(wildcard .env.local)","")
	include .env.local
	export $(shell sed 's/=.*//' .env.local)
endif

ENV_FILE?=.env
ENV_LOCAL_FILE?=.env.local
ENVIRONMENT?=production

BACKEND_PACKAGE_NAME?=backend
BACKEND_PACKAGE_VERSION?=0.0.1
BACKEND_INT_PORT?=80
BACKEND_EXT_PORT?=8000
GHCR_LOCATION?=h2optimize-end-of-study-project-hetic


.PHONY: help build run stop logs start buildd clean cleanall startd restartd

ascii: 
	@echo -e "\e[1;35m"                                                                      
	@echo -e "               &&&                                              " 
	@echo -e "             &&& &&&                                            " 
	@echo -e "           &&&      &&&                                         " 
	@echo -e "          &&          &&      &&&&&                             " 
	@echo -e "         &&            &   &&&&&&&&&                            " 
	@echo -e "        &&           &&  &&&&     &&                            " 
	@echo -e "       &            &  &&&         &&                           " 
	@echo -e "      &  & &      && &&            &&                           " 
	@echo -e "     &  &  &     &  &&             &&                           " 
	@echo -e "    && &  &     &  &              &&            &&&             " 
	@echo -e "   && & &&     &  &               &&       &&&&&&&&&&&&&        " 
	@echo -e "  &&   &&     && &               &&     &&&&&         &&&&&     " 
	@echo -e "  &          &&& &              &&    &&&                 &&&   " 
	@echo -e " &&          &&  &             &&    &&&        &&&&&&&&&&  &&  " 
	@echo -e " &&          &&  &           &&  &  &&         &    &&&&     && " 
	@echo -e " &&          &&  &&        &&  &&&  &&        &   &&         && " 
	@echo -e " &&           &&  &&&   &&&  &&& &  &&       &  &&           && " 
	@echo -e "  &&           &&&  &&&&   &&   &&  &&      &  &&&&          && " 
	@echo -e "  &&&            &&&    &&&    &&   &&     & &&&             && " 
	@echo -e "   &&&             &&&&&&      &&    &&   &&&               &&  " 
	@echo -e "    &&&&                   &&&&       && &                &&&   " 
	@echo -e "      &&&&&&            &&&&&&         &&&              &&&&    " 
	@echo -e "        &&&&&&&&&&&&&&&&&&&&             &&&&&&&&&&&&&&&&&      " 
	@echo -e "\e[0m"
                                                                      
help:
	$(MAKE) ascii
	@echo -e "\e[1;34m#  Commandes principales pour lancer le projet\e[0m"
	@echo -e "\e[36m  make build              \e[0m => Build + start projet avec rebuild"
	@echo -e "\e[36m  make buildd             \e[0m => Build + start projet en mode detache"
	@echo -e "\e[36m  make start              \e[0m => Demarrage rapide (up --build)"
	@echo -e "\e[36m  make startd             \e[0m => Demarre en detache + logs"
	@echo -e "\e[36m  make logs               \e[0m => Logs en temps reel (backend)"

	@echo ""
	@echo -e "\e[1;32m#  Backend\e[0m"
	@echo -e "\e[36m  make buildback          \e[0m => Build image backend vers GHCR"
	@echo -e "\e[36m  make runback            \e[0m => Run image backend localement"
	@echo -e "\e[36m  make pushback           \e[0m => Push image backend vers GHCR"
	@echo -e "\e[36m  make pipinstall LIB=pkg \e[0m => Installer une lib Python dans le conteneur"
	@echo -e "\e[0m                               /!\ METTRE A JOUR 'app\pyproject.toml'"

	@echo ""
	@echo -e "\e[1;31m#  Maintenance\e[0m"
	@echo -e "\e[36m  make cleanall           \e[0m => Supprime containers + volumes"
	@echo -e "\e[36m  make restartd           \e[0m => Clean + Build + Logs"
	
	@echo ""
	@echo -e "\e[35m-------------------------------------------------------------------------------\e[0m"
	@echo -e "\e[1;31m NEXT STEP RECOMMAND : make startd\e[0m"
	@echo -e ""
	@echo -e "\e[34m API :                    \e[0m\e[32mhttp://localhost:$(BACKEND_EXT_PORT)\e[0m"
	@echo -e "\e[34m API Documentation :      \e[0m\e[32mhttp://localhost:$(BACKEND_EXT_PORT)/docs\e[0m"
	@echo -


start :
	docker compose --env-file $(ENV_FILE) --env-file $(ENV_LOCAL_FILE) up -d

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
	$(MAKE) ascii
	$(MAKE) buildd
	$(MAKE) logs

restartd:
	$(MAKE) clean
	$(MAKE) buildd
	$(MAKE) logs

pipinstall:
	@echo -e "\e[1;31m/!\ METTRE A JOUR 'app\pyproject.toml'\e[0m"
	docker compose exec backend sh -c "pip install $(LIB) && pip freeze > /code/app/requirements.txt"

lint:
	docker compose exec backend sh -c "ruff check"

buildback :
	docker build --build-arg BACKEND_INT_PORT=$(BACKEND_INT_PORT) --build-arg ENVIRONMENT=$(ENVIRONMENT) -t ghcr.io/$(GHCR_LOCATION)/$(BACKEND_PACKAGE_NAME):v$(BACKEND_PACKAGE_VERSION) -f ./Dockerfile

runback :
	docker run --env-file .env --env-file .env.local -p $(BACKEND_EXT_PORT):$(BACKEND_INT_PORT) -d ghcr.io/$(GHCR_LOCATION)/$(BACKEND_PACKAGE_NAME):v$(BACKEND_PACKAGE_VERSION) 

pushback :
	docker push ghcr.io/$(GHCR_LOCATION)/$(BACKEND_PACKAGE_NAME):v$(BACKEND_PACKAGE_VERSION)


test:
	docker compose exec backend sh -c "ptw . -vvs"

coverage:
	docker compose exec backend sh -c "pytest -v --cov=app/src --cov-report=term-missing --cov-report=html"


