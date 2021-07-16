# Hearty
A backend API to support hearty.

# Contributing

## Dependencies

1. Python 3.8 - recommend installing using [pyenv](https://github.com/pyenv/pyenv) or 
   [pyenv-win](https://github.com/pyenv-win/pyenv-win)
1. NodeJS - recommend installing using [nvm](https://github.com/nvm-sh/nvm) or 
   [nvm-windows](https://github.com/coreybutler/nvm-windows)
1. Poetry - recommend installing using [their primary instructions](https://python-poetry.org/docs/#installation)
1. Docker - used for consistent deployment artifact packaging. Recommend installing 
   [Docker for Desktop](https://www.docker.com/products/docker-desktop)
and may require installing [WSL2 on Windows](https://docs.microsoft.com/en-us/windows/wsl/install-win10)

## Building and Deploying
This project is using [Serverless Framework](https://www.serverless.com/) for deployment to AWS. 
Serverless is installed as a **local** NPM package, and therefore should be invoked via `npx`

### Makefile
It's recommended to use the `Makefile` commands instead of interacting directly with the tools.
1. `make build` - performs `poetry install` and `npm install`
1. `make test` - runs Python tests
1. `make black` - format application and test directories using [Black](https://github.com/psf/black)
1. `make check` - runs Python tests and Black, mypy, flake8, etc.
1. `make deploy-all stage={stage}` - deploys all components, making the following `make deploy*` commands duplicative
1. `make deploy-core stage={stage}` - runs `serverless deploy` for the core infrastructure stack
1. `make-deploy-apps stage={stage}` - runs `serverless deploy` for the business apps that depend on the core infrastructure
1. `make docs stage={sage}` - generates JSON schema and OpenAPI yml files for public API endpoints

## Components

1. [AWS API Gateway HTTP API](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api.html)
1. [AWS Cognito User Pool](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-identity-pools.html)
1. [Cognito Authorizer](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-jwt-authorizer.html)

### Endpoints / Lambda Functions

1. `/echo` - simply logs and returns request event. Can be used to test authorization.


# Hacks in place

A list of things likely related to this development initiating on a Windows 10 machine.

1. `pythonBin` in [serverless.yml](./serverless.yml) to get `serverless-python-requirements` to work
1. Editing of `poetry.js` from `serverless-python-requirements` per 
   [this GitHub issue](https://github.com/UnitedIncome/serverless-python-requirements/issues/609)
