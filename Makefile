.DEFAULT_GOAL := help

help: ## Show this help message
	@echo "Usage: make [command]"
	@echo ""
	@echo "Commands:"
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'

run:
	#poetry run uvicorn main:app --host 0.0.0.0 --port 8000 --reload --env-file $(ENV_FILE)
	poetry run uvicorn main:app --host 0.0.0.0 --port 8000 --reload

install:  ## Install a dependency using poetry
	@echo "Installing dependency $(LIBRARY)"
	poetry add $(LIBRARY)

migrate-create:
	alembic revision --autogenerate -m $(MIGRATON)

migrate-apply:
	alembic upgrade head

uninstall: ## Uninstall a dependency using poetry
	@echo "Uninstalling dependency $(LIBRARY)"
	poetry remove $(LIBRARY)