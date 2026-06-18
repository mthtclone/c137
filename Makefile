format:
	black .
	ruff check . --fix

lint:
	ruff check .

hooks:
	pre-commit run --all-files