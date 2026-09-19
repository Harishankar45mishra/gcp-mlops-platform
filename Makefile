SHELL := /bin/bash

# ============================================================================
# Project Configuration
# ============================================================================

PROJECT_ID := project-cd87c2b0-43f1-4451-809
DB_HOST := 127.0.0.1
DB_PORT := 5432
DB_NAME := mlflowdb
DB_USER := mlflow
DB_SECRET_NAME := mlflow-db-password
ARTIFACT_ROOT := gs://mlops-platform-artifacts-dev

# ============================================================================
# Targets
# ============================================================================

.PHONY: install sync train run test lint format clean \
	proxy mlflow-db mlflow mlflow-version

install:
	uv sync

sync:
	uv sync

train:
	uv run python training/train.py

run:
	uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

test:
	uv run pytest

lint:
	uv run ruff check .

format:
	uv run ruff format .

clean:
	rm -rf .pytest_cache __pycache__
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

proxy:
	cloud-sql-proxy $(PROJECT_ID):us-central1:mlflow

mlflow-db:
	@DB_PASSWORD="$$(gcloud secrets versions access latest --secret=$(DB_SECRET_NAME))"; \
	ENCODED_PASSWORD="$$(python3 -c 'from urllib.parse import quote; import sys; print(quote(sys.argv[1], safe=""))' "$$DB_PASSWORD")"; \
	uv run mlflow db upgrade "postgresql+psycopg2://$(DB_USER):$$ENCODED_PASSWORD@$(DB_HOST):$(DB_PORT)/$(DB_NAME)"

mlflow:
	@DB_PASSWORD="$$(gcloud secrets versions access latest --secret=$(DB_SECRET_NAME))"; \
	ENCODED_PASSWORD="$$(python3 -c 'from urllib.parse import quote; import sys; print(quote(sys.argv[1], safe=""))' "$$DB_PASSWORD")"; \
	uv run mlflow server \
		--backend-store-uri "postgresql+psycopg2://$(DB_USER):$$ENCODED_PASSWORD@$(DB_HOST):$(DB_PORT)/$(DB_NAME)" \
		--default-artifact-root "$(ARTIFACT_ROOT)" \
		--host 0.0.0.0 \
		--port 5000 \
		--allowed-hosts "*" \
		--cors-allowed-origins "*"

mlflow-version:
	uv run mlflow --version
