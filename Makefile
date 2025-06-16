.PHONY: up down

up:
	docker-compose up -d

down:
	docker-compose down

make restart:
	docker-compose down && docker-compose up -d
logs:
	docker-compose logs -f

build:
	docker-compose build

pull:
	git pull
help:
	@echo "Available commands:"
	@echo "  make up     - Start the Docker containers"
	@echo "  make down   - Stop the Docker containers"
	@echo "  make logs   - View logs of the Docker containers"
	@echo "  make help   - Show this help message"