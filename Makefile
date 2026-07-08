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

env-manager-up:
	docker-compose -f docker-compose.tools.yml up -d --build

env-manager-down:
	docker-compose -f docker-compose.tools.yml down

mongo-ui-up:
	docker run -d \
		--name generate-question-mongo-express \
		--network rocketchat-compose_default \
		-p 8889:8081 \
		-e ME_CONFIG_MONGODB_URL="mongodb://gquser:generateQuestion2025@rocketchat-compose-mongodb-1:27018/quiz?authSource=admin" \
		-e ME_CONFIG_BASICAUTH=false \
		mongo-express:latest

mongo-ui-down:
	docker rm -f generate-question-mongo-express

help:
	@echo "Available commands:"
	@echo "  make run            - Start the Docker containers"
	@echo "  make stop           - Stop the Docker containers"
	@echo "  make restart        - Restart the Docker containers"
	@echo "  make build          - Build the Docker images"
	@echo "  make build-no-cache - Build without using cache"
	@echo "  make clean          - Remove containers, images, and volumes"
	@echo "  make prune          - Clean up all Docker resources"
	@echo "  make pull               - Pull the latest changes from the repository"
	@echo "  make logs               - View logs of the Docker containers"
	@echo "  make env-manager-up     - Start the .env manager UI on port 8888"
	@echo "  make env-manager-down   - Stop the .env manager UI"
	@echo "  make mongo-ui-up        - Start mongo-express DB UI on port 8889"
	@echo "  make mongo-ui-down      - Stop mongo-express DB UI"
	@echo "  make help               - Show this help message"
	@echo ""
	@echo "Environment: $(ENV) (using $(COMPOSE_FILE))"