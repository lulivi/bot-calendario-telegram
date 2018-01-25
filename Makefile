test:
	python setup.py test


clean:
	@rm -rf .Python MANIFEST build dist venv* *.egg-info *.egg .cache .coverage .eggs
	@find . -type f -name "*.py[co]"	-delete
	@find . -type d -name "__pycache__" -delete

.PHONY: test clean
