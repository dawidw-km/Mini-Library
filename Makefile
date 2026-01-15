.PHONY: build up down restart logs test shell clean migrate seed full-build help

COMPOSE := docker compose

help:
	@echo "\033[36mCommands: make + command\033[0m"  # nagłówek cyan
	@echo "\033[94mbuild       \033[32mBuild Docker images\033[0m"
	@echo "\033[94mup          \033[32mStart full stack (db -> migrate -> seed -> api)\033[0m"
	@echo "\033[94mdown        \033[32mStop containers\033[0m"
	@echo "\033[94mrestart     \033[32mRestart containers\033[0m"
	@echo "\033[94mlogs        \033[32mView logs\033[0m"
	@echo "\033[94mtest        \033[32mRun pytest inside api container\033[0m"
	@echo "\033[94mshell       \033[32mOpen shell inside api container\033[0m"
	@echo "\033[94mclean       \033[32mRemove containers, volumes, images\033[0m"
	@echo "\033[94mmigrate     \033[32mRun migrations\033[0m"
	@echo "\033[94mfull-build  \033[32mFirst-time full build\033[0m"
	@echo "\033[94mrevision    \033[32mCreate new migration from model changes\033[0m"




build:
	$(COMPOSE) build

## Start full stack (db -> migrate -> seed -> api)
up:
	$(COMPOSE) up -d

## Stop containers
down:
	$(COMPOSE) down

## Restart everything
restart: down up

## View logs
logs:
	$(COMPOSE) logs -f

## Run pytest inside api container
test:
	$(COMPOSE) exec api python -m pytest -p no:logging -p no:warnings

## Open shell inside api container
shell:
	$(COMPOSE) exec api bash

## Remove containers, volumes, images
clean:
	$(COMPOSE) down -v --rmi local

## Run migrations (one-shot container)
migrate:
	$(COMPOSE) up migrate

## Run seed (one-shot container)
seed:
	$(COMPOSE) up seed

## First-time full build
full-build: build up

## Create new migration from model changes
revision:
	$(COMPOSE) exec api alembic revision --autogenerate -m "$(msg)"
