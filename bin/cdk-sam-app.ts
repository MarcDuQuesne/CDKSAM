#!/usr/bin/env node

import * as cdk from "aws-cdk-lib";

import { CDK2SAMStack } from "../lib/cdk-sam";

const app = new cdk.App();
new CDK2SAMStack(app, "CDK2SAMStack", {
  env: {
    account: "000000000000",
    region: "eu-west-1",
  },
});
