
install:
	pipenv install --dev

test:
	pipenv run pytest -vv

install-package-in-venv:
	pipenv uninstall --skip-lock tqwgp-parser || true
	pipenv run python setup.py install

test-package-in-venv: install-package-in-venv test

format:
	pipenv run black .

release:
	rm -rf build/ dist/
	pipenv run python setup.py sdist
	pipenv run python setup.py bdist_wheel --universal
	pipenv run twine check dist/*
	pipenv run twine upload dist/*

show:
	pipenv run python -m tqwgp_parser show ./tests/samples/16-TESLA-01
