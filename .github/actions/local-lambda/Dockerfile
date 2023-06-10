FROM amazon/aws-lambda-python:latest
ARG input_folder

COPY $input_folder /var/task/
WORKDIR /var/task

RUN if [ -f "requirements.txt" ]; then pip install -r requirements.txt; fi