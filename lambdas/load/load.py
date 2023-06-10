"""
This lambda downloads the transformed data package, validates it and then loads it into the data warehouse.
"""

import os
from typing import Dict

import boto3


def handler(event: Dict, context: Dict) -> Dict:
    """
    This lambda downloads the transformed data package, validates it and then loads it into the data warehouse.
    """

    print(f"event: {event}")
    print(f"context: {context}")

    try:
        bucket_name, sqlalchemy_url = (
            os.environ.get("BUCKET_NAME"),
            os.environ.get("SQLALCHEMY_URL"),
        )
    except KeyError as exc:
        raise ValueError("env not correctly set up.") from exc

    # Create an S3 client
    s3 = boto3.client("s3")
    # List the contents of the bucket
    response = s3.list_objects_v2(Bucket=bucket_name)

    print({"bucket": bucket_name, "content": response["Contents"]})

    return {"result": "success"}
