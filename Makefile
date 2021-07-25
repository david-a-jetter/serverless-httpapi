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

new-environment:
	aws cloudformation validate-template --template-body file://core-cf.yml
	aws cloudformation create-stack --stack-name hearty-core-$(stage) --template-body file://core-cf.yml --parameters ParameterKey=Environment,ParameterValue=$(stage)

deploy-core:
	aws cloudformation validate-template --template-body file://core-cf.yml
	aws cloudformation update-stack --stack-name hearty-core-$(stage) --template-body file://core-cf.yml --parameters ParameterKey=Environment,ParameterValue=$(stage)

deploy-apps:
	npx sls deploy --config serverless.client.yml --stage $(stage)
	npx sls deploy --config serverless.admin.yml --stage $(stage)

deploy-all: deploy-core deploy-apps

docs:
	poetry run python doc/generate_schema.py
	npx sls openapi generate --config serverless.client.yml --stage $(stage) --output openapi.client.yml
	npx sls openapi generate --config serverless.admin.yml --stage $(stage) --output openapi.admin.yml
