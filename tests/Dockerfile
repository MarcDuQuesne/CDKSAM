FROM amazon/aws-lambda-python:latest

COPY lambdas/validate/requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt

COPY lambdas/validate/validate.py ./validate.py

CMD [ "validate.validate_csv_file" ]