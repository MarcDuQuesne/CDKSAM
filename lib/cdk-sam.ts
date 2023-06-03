import * as cdk from "aws-cdk-lib";
import * as lambda from "aws-cdk-lib/aws-lambda";
import * as path from "path";
import * as sfn from "aws-cdk-lib/aws-stepfunctions";
import * as tasks from "aws-cdk-lib/aws-stepfunctions-tasks";

import { Construct } from "constructs";

export class CDK2SAMStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // const bucketName = cdk.Fn.importValue(`${props.dataStackName}-BucketName`);
    // const bucket = s3.Bucket.fromBucketName(this, "bucket", bucketName);

    const loader = new lambda.Function(this, "LoadingLambda", {
      runtime: lambda.Runtime.PYTHON_3_8,
      code: lambda.Code.fromAsset(path.join(__dirname, "../lambda/load")),
      handler: "load.handler",
      timeout: cdk.Duration.minutes(15),
      environment: {
        BUCKET_NAME: "bucket_name",
        SQLALCHEMY_URL: "sqlalchemyUrl",
      },
    });

    const loadingTask = new tasks.LambdaInvoke(this, "loading_task", {
      lambdaFunction: loader,
      resultPath: "$",
      outputPath: "$.Payload",
    });

    const success = new sfn.Succeed(this, "File was processed successfully.");
    const definition = sfn.Chain.start(loadingTask).next(success);

    const stepFunction = new sfn.StateMachine(this, "ETL", {
      definition,
      timeout: cdk.Duration.minutes(15),
    });
  }
}
