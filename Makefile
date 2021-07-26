stage=dev
coreTemplate=file://core-cf.yml
stackPolicy=file://cf/stack-policy.json

build:
	poetry install
	npm install

black:
	poetry run black hearty
	poetry run black tests

test:
	poetry run python -m pytest --cov=hearty tests

check: test
	poetry run mypy hearty tests
	poetry run flake8 hearty
	poetry run flake8 tests
	poetry run black --check hearty
	poetry run black --check tests
	npx sls print --config serverless.client.yml --stage dev
	npx sls print --config serverless.admin.yml --stage dev

set-core-stack-policy:
	aws cloudformation set-stack-policy --stack-name hearty-core-$(stage) --stack-policy-body $(stackPolicy)

new-environment:
	aws cloudformation validate-template --template-body $(coreTemplate)
	aws cloudformation create-stack --stack-name hearty-core-$(stage) \
--template-body $(coreTemplate) --parameters ParameterKey=Environment,ParameterValue=$(stage) \


deploy-core: set-core-stack-policy
	aws cloudformation validate-template --template-body $(coreTemplate)
	aws cloudformation update-stack --stack-name hearty-core-$(stage) \
--template-body $(coreTemplate) --parameters ParameterKey=Environment,ParameterValue=$(stage)

deploy-apps:
	npx sls deploy --config serverless.client.yml --stage $(stage)
	npx sls deploy --config serverless.admin.yml --stage $(stage)

deploy-all: deploy-core deploy-apps

docs:
	poetry run python doc/generate_schema.py
	npx sls openapi generate --config serverless.client.yml --stage $(stage) --output openapi.client.yml
	npx sls openapi generate --config serverless.admin.yml --stage $(stage) --output openapi.admin.yml
