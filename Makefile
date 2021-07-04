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

package:
	npx sls package

deploy:
	npx sls deploy -c serverless.yml -p .serverless -s $(stage)