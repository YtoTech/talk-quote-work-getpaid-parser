
install:
	pipenv install --dev

test:
	pipenv run pytest -vv

format:
	pipenv run black .

release:
	rm -rf build/ dist/
	pipenv run python -m build
# 	pipenv run python setup.py sdist
# 	pipenv run python setup.py bdist_wheel --universal
	pipenv run twine check dist/*
	pipenv run twine upload dist/*

show:
	pipenv run python -m tqwgp_parser show ./tests/samples/16-TESLA-01
