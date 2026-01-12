.PHONY: build up down restart logs test shell clean migrate seed full-build

COMPOSE := docker compose

## Build Docker images
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
