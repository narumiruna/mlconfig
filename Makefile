install:
	poetry install

lint:
	poetry run flake8 -v

test:
	poetry run pytest -v -s --cov=mlconfig tests
