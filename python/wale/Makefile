.PHONY: clean test lint build install release

REQS_PROD=requirements.txt
REQS_DEV=requirements-dev.txt
VENV_NAME = .venv

clean:
	rm -rf build/ dist/ *.egg-info

test:
	pytest

lint:
	flake8 wale

build:
	pip-compile requirements.in
	pip-compile requirements-dev.in
	python setup.py sdist bdist_wheel

setup:
	@echo "Setting up Python virtual environment..."
	python -m venv $(VENV_NAME)
	@echo "Activating Python virtual environment..."
	. $(VENV_NAME)/bin/activate
	pip install -r $(REQS_PROD)
	pip install -r $(REQS_DEV)

.PHONY: release
release:
	bumpversion patch --allow-dirty --verbose
	# Build the distribution packages
	python setup.py sdist bdist_wheel
	# Upload the packages to PyPI
	twine upload dist/*
