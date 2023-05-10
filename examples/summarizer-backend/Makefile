VENV_NAME = .venv
VENV_ACTIVATE = . $(VENV_NAME)/bin/activate

.PHONY: all setup test run install update clean

all: setup run

setup:
	@echo "Setting up Python virtual environment..."
	python -m venv $(VENV_NAME)
	@echo "Activating Python virtual environment..."
	$(VENV_ACTIVATE) && pip install --upgrade pip && pip install pip-tools
	@echo "Python virtual environment setup complete."
	$(VENV_ACTIVATE) && pip install -r requirements.txt
	@echo "Pip dependencies installed"

test:
	@echo "Running tests..."
	$(VENV_ACTIVATE) && pytest tests/

run:
	@echo "Starting server..."
	$(VENV_ACTIVATE) && uvicorn main:app --host 0.0.0.0 --port 8000

update:
	@echo "Updating dependencies..."
	$(VENV_ACTIVATE) && pip-compile --upgrade requirements.in
	@echo "Installing dependencies..."
	$(VENV_ACTIVATE) && pip install -r requirements.txt

