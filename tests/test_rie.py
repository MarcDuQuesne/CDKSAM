
"""Testing the Lambda function locally with the Runtime Interface Emulator (RIE)"""

import docker
import pytest
import requests
from docker.client import DockerClient
from docker.models.containers import Container
import os

from typing import Callable

# Get the current directory
current_dir = os.path.abspath(os.path.dirname(__file__))


@pytest.fixture(scope="session")
def docker_client() -> DockerClient:
    yield docker.from_env()


@pytest.fixture(scope="session")
def docker_image(docker_client: DockerClient):

    image_name = "validation-lambda-local"

    # Build the Docker image
    image, _ = docker_client.images.build(
        path=os.path.join(current_dir, "../"),
        dockerfile="tests/Dockerfile",
        tag=image_name,
        rm=True  # Remove intermediate containers
    )

    return image.id


@pytest.fixture(scope="session")
def start_local_lambda(docker_client: DockerClient, docker_image: str) -> Container:

    container = docker_client.containers.run(docker_image, detach=True, ports={"8080": "9000"})

    yield container

    # Code after the `yield` statement will execute after the tests are done
    container.stop()
    container.remove()


@pytest.fixture(scope="session")
def lambda_url(start_local_lambda: Container):
    return "http://0.0.0.0:9000/2015-03-31/functions/function/invocations"

@pytest.fixture(scope="session")
def invoke_lambda(lambda_url):
    def invoke(payload):
        response = requests.post(lambda_url, json=payload)
        assert response.status_code == 200
        return response
    return invoke


def test_lambda_function(invoke_lambda: Callable):
  payload = {}  # Your JSON payload for invoking the Lambda function
  response = invoke_lambda(payload)
  assert response.status_code == 200
  # Add additional assertions to validate the response or expected behavior