FROM amazon/aws-lambda-python:latest

COPY lambda/validate/requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt

COPY lambda/validate/validate.py ./validate.py

CMD [ "validate.handler" ]