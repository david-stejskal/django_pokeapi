PY_FILES = `find django_pokeapi \
		-path './.cache' -prune -o \
		-path './docs' -prune -o \
		-path './build' -prune -o \
		-path './scripts' -prune -o \
		-path './.eggs' -prune -o \
		-path '**migrations' -prune -o \
		-name '*.py' -print`;


PROJECT_FOLDER=django_pokeapi

## Format

.PHONY: black isort format

black: 
	black $(PROJECT_FOLDER)

isort: 
	isort --profile black $(PROJECT_FOLDER)

format: black isort 


## CI Lint Check

.PHONY: black-ci isort-ci pylint pylint-shorter lint

black-ci: 
	echo -e "\n# Diff for each file:";
	black --diff $(PROJECT_FOLDER)
	echo -e "\n# Status:";
	black --check $(PROJECT_FOLDER)

isort-ci: ## Check import orders
	isort --profile black --check-only $(PROJECT_FOLDER)

pylint: ## Check python source code
	python3 -m pylint $(PY_FILES)

pylint-shorter: ## Check python source code with short output
	python3 -m pylint --disable=I --enable=useless-suppression $(PY_FILES)

lint: black-ci isort-ci pylint-shorter ## Lint check [black, flake8, pylint-shorter, isort-check]
