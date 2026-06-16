.DEFAULT_GOAL = help

.PHONY: setup
setup:  ## Set up the development environment
	uv sync --frozen
	uv run pre-commit install
	uv run playwright install
	(cd streamlit_arborist/frontend && npm clean-install)

.PHONY: backend
backend:  ## Run the Streamlit backend
	STREAMLIT_ARBORIST_DEV=true uv run streamlit run app/example.py

.PHONY: frontend
frontend:  ## Start the frontend development server
	(cd streamlit_arborist/frontend && npm run start)

.PHONY: tests
tests:  ## Run end-to-end tests
	STREAMLIT_ARBORIST_DEV=true uv run pytest --headed --browser firefox

.PHONY: lint
lint:  ## Run pre-commit hooks on the codebase
	uv run pre-commit run --all-files

.PHONY: build
build:  ## Build the frontend assets and the Python package
	(cd streamlit_arborist/frontend && npm run build)
	uv build

.PHONY: help
help:  ## Show this help message
	@printf "\033[32mUsage:\033[0m \033[36mmake <COMMAND>\033[0m\n"
	@echo ""
	@printf "\033[32mCommands:\033[0m\n"
	@grep -E '^[a-z-]+:.*##' $(MAKEFILE_LIST) | awk -F ':.*## ' '{ printf "  \033[36m%-11s\033[0m %s\n", $$1, $$2 }'
