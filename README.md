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

## Docker

A first way of testing the lambda function is to use docker.

```bash
docker build -t lambda-local -f tests/Dockerfile .
```

```bash
docker run --rm -p 9000:9000 lambda-local:latest
```

```bash
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'
```

## SAM: Local test setup

- Synthesize a template and write it to template.yaml

```bash
cdk synth --no-staging
```

The AWS SAM CLI provides support for building Lambda functions and layers defined in your AWS CDK application.
First, activate a python 3.8 environment:

```bash
conda activate stepfunctions-demo
```

```bash
sam build -t ./cdk.out/CDK2SAMStack.template.json
```

sam build doesn't support bundled assets

- Test the lambda function with SAM

```bash
sam local invoke --env-vars local-test-env.json ValidatingLambda --no-event -t ./cdk.out/CDK2SAMStack.template.json
```

## TODO use moto3 to mock out calls to e.g. s3.

# maybe using a context variable:

# https://docs.aws.amazon.com/cdk/latest/guide/context.html

# or maybe - create a wrapper round sam local invoke that does this:

# scans the template for lambda functions

# adds the mocking code to the lambda function

# runs sam local invoke

# SLS-DEV-Tools

```bash
npm install -g sls-dev-tools
```
