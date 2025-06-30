.PHONY: up down

run:
	docker-compose up -d

stop:
	docker-compose down

make restart:
	docker-compose down && docker-compose up -d
logs:
	docker-compose logs -f

build:
	docker-compose build

clean:
	docker-compose down --rmi all --volumes --remove-orphans

pull:
	git pull
help:
	@echo "Available commands:"
	@echo "  make up     - Start the Docker containers"
	@echo "  make down   - Stop the Docker containers"
	@echo "  make restart - Restart the Docker containers"
	@echo "  make build  - Build the Docker images"
	@echo "  make pull   - Pull the latest changes from the repository"
	@echo "  make logs   - View logs of the Docker containers"
	@echo "  make help   - Show this help message"