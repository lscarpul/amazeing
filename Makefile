# Makefile for the a-maze-ing project

# --- Variables ---
PYTHON = python3
LINT_TARGETS = a_maze_ing.py mazegen/
MYPY_FLAGS = --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
FLAKE_FLAGS = --max-line-length=150
TAR_NAME = mazegen.tar.gz
TAR_SRC = mazegen

# --- Rules ---
.PHONY: all clean fclean re install lint run debug build

all: install

install:
	$(PYTHON) -m pip install -r requirements.txt

build:
	$(PYTHON) -m pip install --upgrade build
	$(PYTHON) -m build

tar:
	tar -czvf $(TAR_NAME) $(TAR_SRC)/
	
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
	rm -rf maze.txt

fclean: clean
	rm -rf build/ dist/ *.egg-info $(TAR_NAME)

re: fclean all


