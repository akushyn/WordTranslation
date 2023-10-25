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
