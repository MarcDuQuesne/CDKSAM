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

### Part I: Unit tests

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

### Part II: The Runtime Interface Emulator (RIE)

To test the entire lambda function, instead of only the runtime code inside the handler, we can build and run the docker image locally.

Build the image using:

```bash
docker build -t lambda-local -f tests/Dockerfile .
```

Then run it on port 9000.

```bash
docker run --rm -p 9000:8080 lambda-local:latest
```

To verify that the lambda is listening run the following command from another terminal:

```bash
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'
```

This sends and empty event to the lambda which then responds with an error message. In the terminal running the docker container we see the log of the lambda invocation (just as we would see in CloudWatch).

To run the tests described in the article, activate a Python environment (see part I above), install docker `pip install docker` and run the tests (also make sure you stop the docker container that you may have started earlier, we're reusing port 9000):

```bash
python -m pytest tests/test_rie.py
```

## Part III: SAM: Local test setup

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

### Part IV: Localstack

Install localstack:

```
pip install --upgrade localstack
```

Export any relevant env variables (e.g. `DEBUG=1`, or your `LOCALSTACK_API_KEY`) and start localstack:

```
localstack start
``

Install awscli-local:

```
npm install -g aws-cdk-local
```

Finally, deploy your stacks locally:

```
cdklocal bootstrap
cdklocal deploy
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
