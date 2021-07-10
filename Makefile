black:
	poetry run black hearty
	poetry run black tests

build:
	poetry install
	npm install

test:
	poetry run python -m pytest tests

check: test
	poetry run mypy -m hearty
	poetry run black --check hearty
	poetry run black --check tests
	poetry run flake8 hearty
	poetry run flake8 tests

deploy-core:
	npx sls deploy --stage $(stage)

deploy-apps:
	npx sls deploy --config serverless.client.yml --stage $(stage)

deploy-all: deploy-core deploy-apps
