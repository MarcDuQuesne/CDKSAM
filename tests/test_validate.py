""" Tests for the validatation lambda """
import os
import sys

import boto3
import moto
import pytest

# Get the current directory
current_dir = os.path.abspath(os.path.dirname(__file__))

# Add the lambdas directory to the path
sys.path.append(os.path.join(current_dir, ".."))

from lambdas.validate.validate import validate_csv_file


@pytest.fixture()
def s3_event():
    """Generates S3 Event"""

    return {
        "Records": [
            {
                "eventVersion": "2.0",
                "eventSource": "aws:s3",
                "awsRegion": "us-east-1",
                "eventTime": "1970-01-01T00:00:00.000Z",
                "eventName": "ObjectCreated:Put",
                "userIdentity": {"principalId": "EXAMPLE"},
                "requestParameters": {"sourceIPAddress": "0.0.0.0"},
                "responseElements": {
                    "x-amz-request-id": "EXAMPLE123456789",
                    "x-amz-id-2": "EXAMPLE123/5678abcdefghijklambdaisawesome/mnopqrstuvwxyzABCDEFGH",
                },
                "s3": {
                    "s3SchemaVersion": "1.0",
                    "configurationId": "testConfigRule",
                    "bucket": {
                        "name": "validatetestbucket",
                        "ownerIdentity": {"principalId": "EXAMPLE"},
                        "arn": "arn:aws:s3:::validatetestbucket",
                    },
                    "object": {
                        "key": "test.csv",
                        "size": 1024,
                        "eTag": "d41d8cd98f00b204e9800998ecf8427e",
                        "versionId": "096fKKXTRTtl3on89fVO.nfljtsv6qko",
                    },
                },
            }
        ]
    }



def initialize_s3_bucket():
    """Initialize S3 bucket"""

    # create a fake bucket and upload a file to it
    s3 = boto3.resource("s3")
    s3.create_bucket(Bucket="validatetestbucket")
    s3.Object("validatetestbucket", "test.csv").put(Body=open(os.path.join(current_dir, "data/dataset.csv"), "rb"))

@moto.mock_s3
def test_validate_csv_file(s3_event):
    """Test validate_csv_file"""

    # initialize the S3 bucket
    initialize_s3_bucket()

    # call the lambda function handler
    result = validate_csv_file(s3_event, "")

    # check that the result is correct
    assert result["statusCode"] == 200, "Status code is not 200"


if __name__ == "__main__":
    pytest.main(
        [
            __file__,
        ]
    )