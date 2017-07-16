
.PHONY: init
init:
	python setup.py install
	pipenv install --dev

.PHONY: test
test:
	pytest

.PHONY: clean
clean:
	rm -r build dist *.egg-info __pycache__

.PHONY: publish
publish:
	python3 setup.py bdist_wheel && twine upload dist/*
