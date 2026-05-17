# Makefile for the a-maze-ing project

# --- Variables ---
PYTHON = python3
LINT_TARGETS = a_maze_ing.py mazegen/
MYPY_FLAGS = --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
FLAKE_FLAGS = --max-line-length=150

# --- Rules ---
.PHONY: all clean install lint run debug

all: install

install:
	$(PYTHON) -m pip install -r requirements.txt

run:
	$(PYTHON) a_maze_ing.py config.txt

debug:
	$(PYTHON) -m pdb a_maze_ing.py config.txt

lint:
	flake8 $(LINT_TARGETS) $(FLAKE_FLAGS)
	mypy $(LINT_TARGETS) $(MYPY_FLAGS)

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .mypy_cache
