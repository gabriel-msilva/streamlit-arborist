.PHONY: help
help:
	@echo "Available commands:"
	@echo "  setup		Set up the development environment"
	@echo "  backend    Run the Streamlit backend"
	@echo "  frontend   Start the frontend development server"
	@echo "  tests      Run end-to-end tests"
	@echo "  lint       Run pre-commit hooks on the codebase"
	@echo "  build      Build the frontend assets and the Python package"

.PHONY: setup
setup:
	uv sync
	uv run pre-commit install
	uv run playwright install
	(cd streamlit_arborist/frontend && npm clean-install)

.PHONY: backend
backend:
	streamlit run streamlit_arborist/example.py

.PHONY: frontend
frontend:
	(cd streamlit_arborist/frontend && npm run start)

.PHONY: tests
tests:
	uv run pytest --headed --browser firefox

.PHONY: docs
docs:
	uv run --group docs sphinx-build -b html docs/ docs/_build/

.PHONY: lint
lint:
	uv run pre-commit run --all-files

.PHONY: build
build:
	(cd streamlit_arborist/frontend && npm run build)
	uv build
