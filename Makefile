test:
	poetry run mypy -m hearty
	poetry run black --check hearty
	poetry run pytest tests