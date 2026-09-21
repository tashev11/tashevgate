.PHONY: install lint test gate check

install:
	python3 -m pip install -e ".[dev]"

lint:
	ruff check src tests

test:
	pytest -q

gate:
	tashevgate check . --fail-on blocker

check: lint test gate
