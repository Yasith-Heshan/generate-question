.PHONY: build run run-detached

build:
	docker build -t math-backend .

run:
	docker run --rm -p 8000:8000 math-backend

run-d:
	docker run --rm -d -p 8000:8000 math-backend

help:
	@echo "Available commands:"
	@echo "  make build         - Build the Docker image"
	@echo "  make run           - Run the Docker container in the foreground"
	@echo "  make run-d         - Run the Docker container in detached mode"
	@echo "  make help          - Show this help message"