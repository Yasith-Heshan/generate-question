# Load environment variables from .env file
ifneq (,$(wildcard ./.env))
    include .env
    export
endif

# Set the docker-compose file based on ENV variable
ifeq ($(ENV),production)
    COMPOSE_FILE := docker-compose.prod.yml
else
    COMPOSE_FILE := docker-compose.yml
endif

.PHONY: up down

run:
	docker-compose -f $(COMPOSE_FILE) up -d

stop:
	docker-compose -f $(COMPOSE_FILE) down

restart:
	docker-compose -f $(COMPOSE_FILE) down && docker-compose -f $(COMPOSE_FILE) up -d

logs:
	docker-compose -f $(COMPOSE_FILE) logs -f

build:
	docker-compose -f $(COMPOSE_FILE) build

build-no-cache:
	docker-compose -f $(COMPOSE_FILE) build --no-cache

clean:
	docker-compose -f $(COMPOSE_FILE) down --rmi all --volumes --remove-orphans

prune:
	docker system prune -af --volumes

pull:
	git pull
help:
	@echo "Available commands:"
	@echo "  make run            - Start the Docker containers"
	@echo "  make stop           - Stop the Docker containers"
	@echo "  make restart        - Restart the Docker containers"
	@echo "  make build          - Build the Docker images"
	@echo "  make build-no-cache - Build without using cache"
	@echo "  make clean          - Remove containers, images, and volumes"
	@echo "  make prune          - Clean up all Docker resources"
	@echo "  make pull           - Pull the latest changes from the repository"
	@echo "  make logs           - View logs of the Docker containers"
	@echo "  make help           - Show this help message"
	@echo ""
	@echo "Environment: $(ENV) (using $(COMPOSE_FILE))"