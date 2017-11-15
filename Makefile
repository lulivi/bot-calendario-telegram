.PHONY: test

test:
	pytest -v --pylama --cov-report term-missing --cov=bot_calendario_telegram tests/
