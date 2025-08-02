precommit:
	black . --config pyproject.toml
	ruff check . --fix