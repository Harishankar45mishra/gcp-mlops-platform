SHELL := /bin/bash

# ==============================================================================
# Project Configuration
# ==============================================================================

PROJECT_ID ?= project-cd87c2b0-43f1-4451-809
REGION ?= us-central1
SQL_INSTANCE ?= mlflow

DB_HOST ?= 127.0.0.1
DB_PORT ?= 5432
DB_NAME ?= mlflowdb
DB_USER ?= mlflow
DB_SECRET_NAME ?= mlflow-db-password

ARTIFACT_ROOT ?=
# ============================================================================
# Targets
# ============================================================================

.PHONY: install sync train run test lint format clean \
	proxy mlflow-db mlflow mlflow-version
# ==============================================================================
# Targets
# ==============================================================================


PROM_PORT ?= 9090
GRAFANA_PORT ?= 3000

.PHONY: install sync train run test lint format clean \
        proxy mlflow-db mlflow mlflow-version Pro gra \
	argocd

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
	cloud-sql-proxy $(PROJECT_ID):$(REGION):$(SQL_INSTANCE)

mlflow-db:
	@DB_PASSWORD="$$(gcloud secrets versions access latest --secret=$(DB_SECRET_NAME))"; \
	ENCODED_PASSWORD="$$(python3 -c 'from urllib.parse import quote; import sys; print(quote(sys.argv[1], safe=""))' "$$DB_PASSWORD")"; \
	uv run mlflow db upgrade "postgresql+psycopg2://$(DB_USER):$$ENCODED_PASSWORD@$(DB_HOST):$(DB_PORT)/$(DB_NAME)"

mlflow:
		@echo ""
	@echo "========================================"
	@echo "MLflow UI"
	@echo "========================================"
	@echo "MLflow URL: http://$$(kubectl get svc mlflow -n mlflow -o jsonpath='{.status.loadBalancer.ingress[0].ip}'):5000"
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
mlflow-v:
	uv run mlflow --version

Pro:
	@echo "Prometheus: http://$$(kubectl get svc monitoring-kube-prometheus-prometheus -n monitoring -o jsonpath='{.status.loadBalancer.ingress[0].ip}'):9090"

gra:
	@echo "Grafana: http://$$(kubectl get svc monitoring-grafana -n monitoring -o jsonpath='{.status.loadBalancer.ingress[0].ip}')"


############################################
# ArgoCD
############################################

ARGOCD_PORT ?= 8080

.PHONY: argocd argocd-password

argocd:
	@echo "========================================"
	@echo "ArgoCD"
	@echo "========================================"
	@echo "URL      : https://$$(kubectl -n argocd get svc argocd-server -o jsonpath='{.status.loadBalancer.ingress[0].ip}')"
	@echo "Username : admin"
	@echo "Password : $$(kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath='{.data.password}' | base64 -d)"
	@echo ""
	@echo "Opening port-forward..."
	@echo "Press Ctrl+C to stop."
	@echo "========================================"
	@kubectl port-forward svc/argocd-server -n argocd $(ARGOCD_PORT):443

argocd-password:
	@kubectl -n argocd get secret argocd-initial-admin-secret \
	-o jsonpath='{.data.password}' | base64 -d && echo
