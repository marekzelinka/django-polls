run:
    uv run manage.py runserver

typecheck:
    uv run ty check

lint:
    uv run ruff check --fix

format:
    uv run ruff format
