import * as apigw from "aws-cdk-lib/aws-apigateway";
import * as cdk from "aws-cdk-lib";
import * as lambda from "aws-cdk-lib/aws-lambda";
import * as path from "path";
import * as python_lambda from "@aws-cdk/aws-lambda-python-alpha";
import * as sfn from "aws-cdk-lib/aws-stepfunctions";
import * as tasks from "aws-cdk-lib/aws-stepfunctions-tasks";

import { Construct } from "constructs";

export class CDK2SAMStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // We create a simple lambda function that will be used to validate a file from s3.
    const validator = new python_lambda.PythonFunction(this, "ValidatingLambda", {
      entry: path.join(__dirname, "../lambdas/validate"),
      functionName: "ValidatingLambda",
      timeout: cdk.Duration.minutes(15),
      runtime: lambda.Runtime.PYTHON_3_8,
      index: "validate.py",
      handler: "handler",
      environment: {
        BUCKET_NAME: "bucket_name",
      },
    });

    // TODO consider removing this if it gets too complex.
    // the idea was to allow this function (locally) to interact with a local database,
    // when testing with SAM or LocalStack.
    const loader = new python_lambda.PythonFunction(this, "LoadingLambda", {
      entry: path.join(__dirname, "../lambdas/load"),
      functionName: "LoadingLambda",
      timeout: cdk.Duration.minutes(15),
      runtime: lambda.Runtime.PYTHON_3_8,
      index: "load.py",
      handler: "handler",
      environment: {
        BUCKET_NAME: "bucket_name",
        SQLALCHEMY_URL: "sqlalchemyUrl",
      },
    });

    // We create a step function that will orchestrate the validation and loading of the file.

    const validationTask = new tasks.LambdaInvoke(this, "validation_task", {
      lambdaFunction: validator,
      resultPath: "$",
      outputPath: "$.Payload",
    });

    const loadingTask = new tasks.LambdaInvoke(this, "loading_task", {
      lambdaFunction: loader,
      resultPath: "$",
      outputPath: "$.Payload",
    });

    const success = new sfn.Succeed(this, "File was processed successfully.");
    const definition = sfn.Chain.start(validationTask).next(loadingTask).next(success);

    const stepFunction = new sfn.StateMachine(this, "ETL", {
      definition,
      timeout: cdk.Duration.minutes(15),
      stateMachineType: sfn.StateMachineType.EXPRESS,
    });

    // Here we add an API Gateway, a typical serverless pattern
    const api = new apigw.RestApi(this, "ETL_API");

    // Locally testing integrations with Lambda is well supported
    const validatorPath = api.root.addResource("validatorLambda");
    validatorPath.addMethod("ANY", new apigw.LambdaIntegration(validator));

    // But other integrations are not: nor simple mockintegrations ...
    const loaderPath = api.root.addResource("loaderLambda");
    loaderPath.addMethod(
      "ANY",
      new apigw.MockIntegration({
        integrationResponses: [{ statusCode: "200" }],
      }),
      {
        methodResponses: [{ statusCode: "200" }],
      }
    );

    // ... nor stepfunction integrations
    const etlPath = api.root.addResource("ETL");
    etlPath.addMethod("POST", apigw.StepFunctionsIntegration.startExecution(stepFunction));

    // integrations with anything but lambdas are simply ignored when running locally.
    // This is visibile using the --debug flag with sam local start-api
  }
}
