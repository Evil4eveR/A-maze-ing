PY  := python3
URU  := uv run
CFG ?= config.txt
OUT ?= maze.txt
MAZE := a_maze_ing.py
SRC  := src/

run:
	$(URU) $(PY) a_maze_ing.py $(CFG)

install:
	uv sync

test:
	$(URU) pytest -v tests/

debug:
	$(URU) $(PY) -m pdb a_maze_ing.py $(CFG)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .mypy_cache .pytest_cache src/mazegen.egg-info src/build

output:
	$(URU) $(PY) a_maze_ing.py $(CFG) file_only
	@echo "Maze output:"
	@cat $(OUT)

lint:
	$(URU) flake8 src/ $(MAZE)
	$(URU) mypy src/ $(MAZE) --warn-return-any --warn-unused-ignores \
		--ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	$(URU) flake8 src/ $(MAZE)
	$(URU) mypy src/ $(MAZE) --strict

build:
	cd $(SRC) && $(URU) $(PY) setup.py bdist_wheel --dist-dir .. && \
	cd ..

.PHONY: install run test debug clean lint lint-strict output build
