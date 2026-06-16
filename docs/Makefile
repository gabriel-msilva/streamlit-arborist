.DEFAULT_GOAL = help

SOURCE_DIR = .
BUILD_DIR = _build/html
SPHINX_OPTS = --nitpicky --fail-on-warning --keep-going -b html

.PHONY: build
build: ## Build Sphinx docs
	uv run --group docs \
		sphinx-build $(SPHINX_OPTS) $(SOURCE_DIR) $(BUILD_DIR)

.PHONY: clean
clean: ## Remove build artifacts
	rm -rf $(BUILD_DIR)

.PHONY: help
help: ## Show this help message
	@printf "\033[32mUsage:\033[0m \033[36mmake <COMMAND>\033[0m\n"
	@echo ""
	@printf "\033[32mCommands:\033[0m\n"
	@grep -E '^[a-z-]+:.*##' $(MAKEFILE_LIST) | awk -F ':.*## ' '{ printf "  \033[36m%-7s\033[0m %s\n", $$1, $$2 }'
