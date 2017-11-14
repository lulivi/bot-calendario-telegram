.PHONY: install_pip test coverage

pip_install:
	pip install .

test:
	pytest -v --pylama --cov-report term-missing --cov=bot_calendario_telegram tests/

coverage:
	codecov
