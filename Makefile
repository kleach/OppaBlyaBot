ROOT_DIR := $(patsubst %/,%,$(dir $(abspath $(lastword $(MAKEFILE_LIST)))))
WORKDIR := $(ROOT_DIR)
VENVDIR := $(ROOT_DIR)/venv

.PHONY: create-venv
create-venv:
	@echo Creating virtual environment
	@cd $(ROOT_DIR)
	@pyenv exec pip install --upgrade virtualenv
	@pyenv exec virtualenv venv

.PHONY: install-requirements
install-requirements:
	@echo Installing requirements
	$(VENV)/python -m pip install --upgrade -r $(ROOT_DIR)/requirements.txt

.PHONY: install-dev-requirements
install-dev-requirements:
	@echo Installing development requirements
	$(VENV)/python -m pip install --upgrade -r $(ROOT_DIR)/requirements-dev.txt

.PHONY: init-venv
init-venv: create-venv install-requirements

.PHONY: init-dev-venv
init-dev-venv: create-venv install-dev-requirements

.PHONY: freeze-versions
freeze-venv:
	@echo Freezing versions of required packages
	$(VENV)/python -m pip freeze -l -r $(ROOT_DIR)/requirements.in.txt > $(ROOT_DIR)/requirements.txt

.PHONY: freeze-dev-versions
freeze-dev-versions:
	@echo Freezing development versions of required packages
	$(VENV)/python -m pip freeze -l -r $(ROOT_DIR)/requirements-dev.in.txt > $(ROOT_DIR)/requirements-dev.txt

.PHONY: clean
clean: clean-venv

.PHONY: help
help:
	@echo Commands:
	@echo  init-venv                - Initialize virtual environment with installing required packages
	@echo  init-dev-venv            - Initialize virtual environment with installing packages required for development
	@echo  create-venv              - Create virtual environment
	@echo  install-requirements     - Install required packages
	@echo  install-dev-requirements - Install packages required for development
	@echo  freeze-versions          - Freeze versions of required packages
	@echo  freeze-dev-versions      - Freeze versions of packages required for development
	@echo  clean                    - Clean unnecessary files
	@echo  help                     - Show this help message

include Makefile.venv
