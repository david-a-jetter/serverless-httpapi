stage=dev

build:
	poetry install
	npm install

black:
	poetry run black hearty
	poetry run black tests

test:
	poetry run python -m pytest --cov=hearty tests

check:
	poetry run mypy hearty tests
	poetry run flake8 hearty
	poetry run flake8 tests
	make test
	poetry run black --check hearty
	poetry run black --check tests
	npx sls print --stage dev
	npx sls print --config serverless.client.yml --stage dev

deploy-core:
	npx sls deploy --stage $(stage)

deploy-apps:
	npx sls deploy --config serverless.client.yml --stage $(stage)

deploy-all: deploy-core deploy-apps

docs:
	poetry run python doc/generate_schema.py
	npx sls openapi generate --config serverless.client.yml --stage $(stage) --output openapi.client.yml
