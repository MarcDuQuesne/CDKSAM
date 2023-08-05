"""
Lambda function to validate files uploaded to S3
"""

import json
import logging
from typing import Dict

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3_client = boto3.client('s3')


def do_something(event: Dict, context: Dict) -> Dict[str, str]:
    """
    Validate the CSV file uploaded to S3
    """
    # step logic
    return {"statusCode": 200, "body": json.dumps({ "result": "success"})}