FROM ubuntu:focal

RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-pip python3-dev llvm llvm-dev 


WORKDIR /app
COPY . .

RUN pip3 install -r requirements.txt

RUN python3 bootscript.py

EXPOSE 5000 5000
EXPOSE 80 80
EXPOSE 443 443


ENTRYPOINT ["python3", "lambda_function.py"]
