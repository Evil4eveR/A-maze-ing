install:
	uv sync

run:
	uv run python src/a_maze_ing.py config.txt

#for testing, we want to run pytest with the tests/ directory as the target
test:
	uv run pytest -v tests/

debug:
	uv run python -m pdb src/a_maze_ing.py config.txt

clean:
	rm -rf __pycache__ .venv .mypy_cache .pytest_cache \
		src/__pycache__ src/algo/__pycache__ \
		src/models/__pycache__ src/hooks/__pycache__ \
		src/renderer/__pycache__ src/solver/__pycache__ \
		src/utils/__pycache__ tests/__pycache__ tests/test_cell.pyc


lint:
	uv run flake8 . --warn-return-any --warn-unused-ignores \
		--ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
	uv run mypy . --warn-return-any --warn-unused-ignores \
		--ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	uv run flake8 . --strict
	uv run mypy . --strict

.PHONY: install run test debug clean lint lint-strict
