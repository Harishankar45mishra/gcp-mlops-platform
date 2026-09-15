.PHONY: install sync train run test lint format clean

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
	rm -rf .pytest_cache
	rm -rf __pycache__
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

mlflow:
	uv run mlflow server \
  	 --backend-store-uri sqlite:///mlflow.db \
  	 --artifacts-destination gs://mlops-test-1789472404 \
  	 --serve-artifacts \
  	 --host 0.0.0.0 \
  	 --port 5000 \
  	 --allowed-hosts "*" \
	 --cors-allowed-origins "*"
