FROM amazon/aws-lambda-python:latest

COPY lambda/load/requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt

COPY lambda/load/load.py ./load.py

CMD [ "load.handler" ]