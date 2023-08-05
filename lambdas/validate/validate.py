"""
Lambda function to validate files uploaded to S3
"""

import json
import logging
from typing import Dict

import boto3
import pandas as pd
import pandera as pa

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3_client = boto3.client('s3')

# create a DataFrameSchema object that can be used to validate a DataFrame
schema =  pa.DataFrameSchema({
            "temperature": pa.Column(pa.Float),
            "humidity": pa.Column(pa.Float, checks=[
                pa.Check.greater_than_or_equal_to(0),
                pa.Check.less_than_or_equal_to(100)
                ]),
            }, index=pa.Index(pa.DateTime))

def validate_csv_file(event: Dict, context: Dict) -> Dict[str, str]:
    """
    Validate the CSV file uploaded to S3
    """

    print(event, context)

    # Get the object from the event and show its content type
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_info = event['Records'][0]['s3']
    file_key = file_info['object']['key']

    # read file from S3 into DataFrame
    csv_obj = s3_client.get_object(Bucket=bucket_name, Key=file_key)
    body = csv_obj["Body"]
    df = pd.read_csv(body, index_col='datetime', parse_dates=True)

    # if validation does not pass,
    # a SchemaErrors object is raised with a detailed explanation of the error
    schema.validate(df)
    return {"statusCode": 200, "body": json.dumps({ "result": "success"})}
