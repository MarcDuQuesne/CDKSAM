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

## Local test setup
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
sam local invoke --env-vars local-test-env.json LoadingLambda --no-event -t ./cdk.out/CDK2SAMStack.template.json
```



