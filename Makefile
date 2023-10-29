PACKAGE = app
PYTHON = python3.10
TESTS = tests
MIGRATIONS = migrations
PYTEST_OPTS =
VENV = venv
VENV_BIN = $(VENV)/bin
VENV_PRE_COMMIT_BIN = $(VENV).pre-commit/bin
VENV_LINT_BIN = $(VENV).lint/bin

venv: requirements.txt
	rm -rf $@
	$(PYTHON) -m venv $@
	$(VENV_BIN)/pip install -r $<

venv.pre-commit:
	rm -rf $@
	$(PYTHON) -m venv $@
	$(VENV_PRE_COMMIT_BIN)/pip install pre-commit

venv.lint: requirements.txt requirements.lint.txt
	rm -rf $@
	$(PYTHON) -m venv $@
	$(VENV_LINT_BIN)/pip install -r requirements.txt
	$(VENV_LINT_BIN)/pip install -r requirements.lint.txt

.PHONY: update-requirements
update-requirements: packages.txt
	rm -rf $(VENV)
	$(PYTHON) -m venv $(VENV)
	$(VENV_BIN)/pip install -r $<
	$(VENV_BIN)/pip freeze > requirements.txt

.PHONY: pre-commit-install
pre-commit-install: venv.pre-commit
	$(VENV_PRE_COMMIT_BIN)/pre-commit install

.PHONY: pre-commit-autoupdate
pre-commit-autoupdate: venv.pre-commit
	$(VENV_PRE_COMMIT_BIN)/pre-commit autoupdate

.PHONY: pre-commit-run-all
pre-commit-run-all: venv.pre-commit
	$(VENV_PRE_COMMIT_BIN)/pre-commit run --all-files

.PHONY: lint-black
lint-black: venv.lint
	$(VENV_LINT_BIN)/black --check --diff $(PACKAGE) $(TESTS) $(MIGRATIONS)

.PHONY: lint-ruff
lint-ruff: venv.lint
	$(VENV_LINT_BIN)/ruff check $(PACKAGE) $(TESTS) $(MIGRATIONS)

.PHONY: lint-mypy
lint-mypy: venv.lint
	$(VENV_LINT_BIN)/mypy $(PACKAGE)

.PHONY: lint
lint: lint-black lint-ruff lint-mypy

.PHONY: ruff-fix
ruff-fix: venv.lint
	$(VENV_LINT_BIN)/ruff --fix $(PACKAGE) $(TESTS) $(MIGRATIONS)

.PHONY: test
test: venv
	$(VENV_BIN)/pytest $(PYTEST_OPTS) $(TESTS)

.PHONY: test-coverage
test-coverage: venv
	$(VENV_BIN)/pytest $(PYTEST_OPTS) --cov=$(PACKAGE) --cov-report=term $(TESTS)

.PHONY: test-real
test-real: venv
	$(VENV_BIN)/pytest $(PYTEST_OPTS) -m real $(TESTS)

.PHONY: run
run: venv
	$(VENV_BIN)/uvicorn $(PACKAGE).main:app --reload

.PHONY: clean
clean:
	rm -rf `find . -name __pycache__`
	rm -f `find . -type f -name '*.py[co]' `
	rm -f `find . -type f -name '*~' `
	rm -f `find . -type f -name '.*~' `
	rm -f `find . -type f -name '@*' `
	rm -f `find . -type f -name '#*#' `
	rm -f `find . -type f -name '*.orig' `
	rm -f `find . -type f -name '*.rej' `
	rm -f `find . -type f -name '*.egg-info' `
	rm -rf coverage
	rm -rf .coverage
	rm -rf */.pytest_cache
	rm -rf cover
	rm -rf htmlcov
	rm -rf .cache
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .eggs
	rm -rf *.egg-info
	rm -rf venv
	rm -rf venv.pre-commit
	rm -rf venv.lint


.PHONY: help
help:
	@echo "Available targets:"
	@echo
	@echo "venv                   - Create virtual environment and install project dependencies."
	@echo "venv.pre-commit        - Create virtual environment and install pre-commit hooks."
	@echo "venv.lint              - Create virtual environment and install linting dependencies."
	@echo "update-requirements    - Update project dependencies and requirements.txt."
	@echo "pre-commit-install     - Install and configure pre-commit hooks."
	@echo "pre-commit-autoupdate  - Update pre-commit hooks."
	@echo "pre-commit-run-all     - Run all configured pre-commit hooks."
	@echo "lint-black             - Lint the code using the Black code formatter."
	@echo "lint-ruff              - Lint the code using the Ruff linter."
	@echo "lint-mypy              - Lint the code using the MyPy static type checker."
	@echo "lint                   - Run all linting targets (lint-black, lint-ruff, lint-mypy)."
	@echo "ruff-fix               - Automatically fix issues using the Ruff linter."
	@echo "test                   - Run tests using pytest."
	@echo "test-coverage          - Run tests with code coverage analysis using pytest."
	@echo "test-real              - Run tests marked with the 'real' marker."
	@echo "run                    - Start the application using Uvicorn with auto-reloading."
	@echo "clean                  - Remove temporary and generated files and directories."
