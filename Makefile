PYTHON_VERSION=3.12.7

.PHONY: init
init:
	pyenv install -s ${PYTHON_VERSION}
	pyenv local ${PYTHON_VERSION}
	python -m venv .venv
	pip install poetry
	poetry env use $$(pyenv which python)
	poetry install
	poetry shell
	poetry run pre-commit install

.PHONY: activate
activate:
	poetry shell

.PHONY: pre-commit-update
pre-commit-update
	poetry run pre-commit autoupdate
