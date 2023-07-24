ENV=poetry run

# Util commands

lint:
	$(ENV) flake8

test:
	$(ENV) pytest

test-coverage:
	$(ENV) coverage run -m pytest tests
	$(ENV) coverage report --omit=*/tests/*,*/migrations/*
	$(ENV) coverage xml --omit=*/tests/*,*/migrations/*

requirements.txt: 
	poetry export --without-hashes --no-cache --output=requirements.txt


# Main commands (Poetry)

setup:
	poetry install

migrate:
	$(ENV) alembic upgrade head

start:
	$(ENV) python3 -m app.main


# Main commands (Docker)

compose-build:
	docker compose build

compose-up:
	docker compose up