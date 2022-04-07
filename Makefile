tag:
	git tag v$(poetry version -s) && git push origin v$(poetry version -s)
