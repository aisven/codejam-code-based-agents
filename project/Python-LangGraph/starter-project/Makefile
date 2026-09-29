.DEFAULT_GOAL := help
IS_CI:=$(CI)

# disable copying some_script.sh to some_script
%: %.sh

help:       ## Show available options with this Makefile
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

.PHONY: sync
sync:       ## Run uv sync with dev and test extras
	uv sync --extra dev --extra test

.PHONY: format-and-lint-code
format-and-lint-code:       ## Format and lint all code
	uv run ruff format starter_project
	uv run ruff format tests
	uv run ruff check starter_project
	uv run ruff check tests

.PHONY : test
test:       ## Run all the tests
	uv run pytest -vv -s --cov-report term-missing --cov starter_project

.PHONY: run-pipeline
run-pipeline:       ## Run the partially agentic generative pipeline
	uv run --env-file .env python -m starter_project.basic_agent

.PHONY: clean
clean:      ## Clean
	./clean_all.sh
