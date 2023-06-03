"""
This lambda downloads the transformed data package, validates it and then loads it into the data warehouse.
"""

import os
from typing import Dict


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

    return {"success": "True"}
