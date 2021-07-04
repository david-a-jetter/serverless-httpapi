black:
	poetry run black hearty
	poetry run black tests

build:
	poetry install
	npm install

test:
	poetry run mypy -m hearty
	poetry run black --check hearty
	poetry run black --check tests
	poetry run pytest tests

deploy-core:
	npx sls deploy --stage $(stage)

deploy-apps:
	npx sls deploy --config serverless.client.yml --stage $(stage)

deploy-all: deploy-core deploy-apps
