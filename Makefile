VERSION := $(shell poetry version -s)

tag:
	git tag v${VERSION} && git push origin v${VERSION}

test:
	poetry run pytest -v -s tests
