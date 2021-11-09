FROM amazon/aws-lambda-python:3.8

COPY . ${LAMBDA_TASK_ROOT}

RUN pip3 install -r requirements.txt

RUN python3 bootscript.py

CMD ["app.handler"]
