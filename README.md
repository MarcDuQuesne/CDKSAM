# Welcome to CDK SAM

This is a project that defines a serverless ETL, written in the AWS CDK.
We use SAM for local development and testing.

## Contributing

Please see the [CONTRIBUTING.md](CONTRIBUTING.md) file for information on how to contribute to this project.

# Instructions

## Pre requisites

- [Install the CDK](https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html)
- [Install the SAM](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)

- Install the dependencies

```bash
npm install
```

- Compile the typescript to js

```bash
npm run build
```

Configure your account and region for CDK deployment

```bash
cdk bootstrap
```

## Unit tests

### Part I of our Medium article

Testing the code inside the lambda using regular unit tests with `pytest`.

Create a Python virtual env with `pytest, boto3, moto, pandas, pandera`

```bash
python -m venv .env
source .env/bin/activate
pip install pytest boto3 moto pandas pandera
```

Ensure you have a fake AWS credentials file, no real credentials are needed since we mock out AWS resources, but the file needs to exist.

```bash
mkdir ~/.aws && touch ~/.aws/credentials && echo -e "[default]\naws_access_key_id = test\naws_secret_access_key = test" > ~/.aws/credentials
```

Run the tests:

```bash
python -m pytest tests/test_validate.py
```

## Docker

### Part II of our Medium article

A first way of testing the lambda function is to use docker.

```bash
docker build -t lambda-local -f tests/Dockerfile .
```

```bash
docker run --rm -p 9000:8080 lambda-local:latest
```

```bash
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'
```

## SAM: Local test setup

- Synthesize a template and write it to template.yaml

```bash
cdk synth --no-staging > template.yml
```

The AWS SAM CLI provides support for building Lambda functions and layers defined in your AWS CDK application.
First, activate a python 3.8 environment:

```bash
conda activate stepfunctions-demo
```

```bash
sam build
```

sam build doesn't support bundled assets

- Test the lambda function with SAM

```bash
sam local invoke --env-vars local-test-env.json ValidatingLambda --no-event
```

- Test the API gateway with SAM

```bash
sam local start-api --env-vars local-test-env.json --debug
```

Integrations with URI other than Lambda Function are not supported.

To test the lambda function:

```bash
curl -XPOST "http://localhost:3000/validatorLambda" -d '{}'
```

## TODO use moto3 to mock out calls to e.g. s3.

- maybe using a context variable:

- https://docs.aws.amazon.com/cdk/latest/guide/context.html

- or maybe - create a wrapper round sam local invoke that does this:

  - scans the template for lambda functions

  - adds the mocking code to the lambda function

  - runs sam local invoke

# SLS-DEV-Tools

```bash
npm install -g sls-dev-tools
```
