RUN		= uv run
SRC		= src
MAIN	= a_maze_ing.py
CONFIG	= ../config.txt

.PHONY: install run debug clean lint lint-strict

install:
	uv sync

run:
	cd $(SRC) && $(RUN) $(MAIN) $(CONFIG) && cd ..

debug:
	cd $(SRC) && $(RUN) -m pdb $(MAIN) $(CONFIG) && cd ..

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null; true
	rm -rf .mypy_cache

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports \
		--disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict
