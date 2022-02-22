SHELL := bash
PATH := ./venv/bin:${PATH}
PYTHON = python3.8
PROJECT = mati
isort = isort $(PROJECT) tests setup.py
black = black -S -l 79 --target-version py37 $(PROJECT) tests setup.py


all: test

venv:
		$(PYTHON) -m venv --prompt $(PROJECT) venv
		pip install -qU pip

install:
	pip install -qU -r requirements.txt

install-test: install
	pip install -qU -r requirements-test.txt

test: clean install-test lint
		pytest

format:
		$(isort)
		$(black)

lint:
		$(isort) --check-only
		$(black) --check
		flake8 $(PROJECT) tests setup.py
		mypy $(PROJECT) tests

clean:
		find . -name '*.pyc' -exec rm -f {} +
		find . -name '*.pyo' -exec rm -f {} +
		find . -name '*~' -exec rm -f {} +
		rm -rf build dist $(PROJECT).egg-info

release: test clean
		python setup.py sdist bdist_wheel
		twine upload dist/*


.PHONY: all install-test test format lint clean release
