#!/usr/bin/env node

import * as cdk from "aws-cdk-lib";

import { CDK2SAMStack } from "../lib/cdk-sam";

const app = new cdk.App();
new CDK2SAMStack(app, "CDK2SAMStack",
    {
        env: {
            account: process.env.CDK_DEFAULT_ACCOUNT,
            region: process.env.CDK_DEFAULT_REGION,
        },
    }
);
