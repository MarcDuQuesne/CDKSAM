#!/bin/sh

docker build -t my-lambda-image .
docker run my-lambda-image "${1}"