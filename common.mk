# DO NOT EDIT: copied via dev_update. Checksum: de3394cfffa83ba90978937b3a979bde

default: help

# Based on https://gist.github.com/lumengxi/0ae4645124cd4066f676
.PHONY: clean clean-pyc clean-build clean-os clean-test clean-docs
.PHONY: init init-prod init-dev
.PHONY: dev-all dev-update
.PHONY: docs git-clean git-push lint
.PHONY: test test-all test-via-setup
.PHONY: help help-more help-common

define BROWSER_PYSCRIPT
import os, webbrowser, sys
try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT
BROWSER := python -c "$$BROWSER_PYSCRIPT"
PYTHON := ./venv/bin/python3
SYS_PYTHON := python3
DOCS_EXCLUDE :=
DEV_UPDATE := $(PYTHON) -m x7.lib.utils.dev_update
COVERAGE_OMIT :=


# Don't descend into any dotted dirs or venv.  Use like '$(FIND_SKIP) -other -find -args'
FIND_SKIP := find -E . -regex './(\..*|venv).*' -prune -o
PROJECT_DIR := ./x7

help: help-common help-more
help-more:
help-common:
	@echo "clean - remove all build, test, coverage and Python artifacts"
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "clean-test - remove test and coverage artifacts"
	@echo "init - install requirements.txt and dev-requirements.txt"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "test-all - run tests on every Python version with tox"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "dev-all - run make test coverage docs lint"
	@echo "dev-update - auto-update common files from x7-lib"
	@echo "install - install the package to the active Python's site-packages"
	@echo "dist - package"
	@echo "upload-test - package and upload a release to test.pypi"
	@echo "upload-prod - package and upload a release to pypi"
	@echo ""
	@echo "To upload to pypi.org: update __version__.py, commit, push, then 'make upload-prod'"

venv:
	$(SYS_PYTHON) -m venv venv

init: init-prod init-dev

init-prod:
	$(PYTHON) -m pip -q install --upgrade pip
	$(PYTHON) -m pip -q install -r requirements.txt

init-dev:
	$(PYTHON) -m pip -q install -r dev-requirements.txt

clean: clean-build clean-pyc clean-test clean-os clean-docs

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	$(FIND_SKIP) -name '*.egg-info' -exec rm -fr {} +
	$(FIND_SKIP) -name '*.egg' -exec rm -f {} +

clean-os:
	$(FIND_SKIP) -name '.DS_Store' -exec rm -fr {} +

clean-pyc:
	$(FIND_SKIP) -name '*.pyc' -exec rm -f {} +
	$(FIND_SKIP) -name '*.pyo' -exec rm -f {} +
	$(FIND_SKIP) -name '*~' -exec rm -f {} +
	$(FIND_SKIP) -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

clean-docs:
	rm -rf docs/_build
	rm -rf docs/_apidoc

dev-all: dev-update test coverage docs lint

dev-update:
	$(DEV_UPDATE)

lint:
	$(PYTHON) -m flake8 $(PROJECT_DIR) tests

test:
	$(PYTHON) -m unittest discover -s tests -t .

test-via-setup:
	$(PYTHON) setup.py test

test-all:
	tox

coverage:
	coverage run --source $(PROJECT_DIR) -m unittest discover -s tests -t .
	coverage report -m $(COVERAGE_OMIT)
	coverage html $(COVERAGE_OMIT)
	$(BROWSER) htmlcov/index.html

docs:
	rm -rf docs/_apidoc
	sphinx-apidoc -o docs/_apidoc $(PROJECT_DIR) $(DOCS_EXCLUDE)
	rm docs/_apidoc/modules.rst
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html

servedocs: docs
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

git-clean:
	git status | grep --quiet 'nothing to commit, working tree clean' || (git status && exit 1)

git-push:
	git push
	git push --tags

upload-test: git-clean dist
	$(PYTHON) -m twine upload --repository testpypi dist/*

upload-prod: git-clean dist
	git tag -a v`python3 -m setup --version` -m 'Tagging for release'
	$(PYTHON) -m twine upload --repository pypi dist/*
	@echo "Don't forget 'make git-push'"

dist: clean
	$(PYTHON) setup.py sdist
	$(PYTHON) setup.py bdist_wheel
	ls -l dist

install: clean
	$(PYTHON) setup.py install -n
