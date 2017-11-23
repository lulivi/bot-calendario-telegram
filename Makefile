test:
	pytest -v --pylama --cov-report term-missing --cov=bot_calendario_telegram tests/


clean:
	@rm -rf .Python MANIFEST build dist venv* *.egg-info *.egg
	@find . -type f -name "*.py[co]" -delete
	@find . -type d -name "__pycache__" -delete

.PHONY: test clean
