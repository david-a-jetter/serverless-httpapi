# Hearty
A backend API to support hearty.

# Contributing

## Dependencies

1. Python 3.8 - recommend installing using [pyenv](https://github.com/pyenv/pyenv) or [pyenv-win](https://github.com/pyenv-win/pyenv-win)
1. NodeJS - recommend installing using [nvm](https://github.com/nvm-sh/nvm) or [nvm-windows](https://github.com/coreybutler/nvm-windows)
1. Poetry - recommend installing using [their primary instructions](https://python-poetry.org/docs/#installation)

## Building and Deploying

This project is using [Serverless Framework](https://www.serverless.com/) for deployment to AWS. 
Serverless is installed as a **local** NPM package, and therefore should be invoked via `npx`

1. `poetry install` - sets up Poetry-managed virtual environment and installs python packages
1. `npx install` - installs Serverless and any specified plugins
1. `npx sls package` - (optional) creates a local zip file of the Serverless application
1. `npx sls deploy` - deploys Serverless application to AWS, using your default AWS profile

## Components

1. [AWS API Gateway HTTP API](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api.html)
1. [AWS Cognito User Pool](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-identity-pools.html)
1. [Cognito Authorizer](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-jwt-authorizer.html)

### Endpoints / Lambda Functions

1. `/echo` - simply logs and returns request event. Can be used to test authorization.


# Hacks in place

A list of things likely related to this development initiating on a Windows 10 machine.

1. `pythonBin` in [serverless.yml](./serverless.yml) to get `serverless-python-requirements` to work
1. Editing of `poetry.js` from `serverless-python-requirements` per (this GitHub issue)[https://github.com/UnitedIncome/serverless-python-requirements/issues/609]
