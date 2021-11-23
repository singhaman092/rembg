Deployment Steps Order Wise

## docker build ##
docker build -t rembg .

## gcp auth ##
gcloud auth login
gcloud config set project leaguecards-dev-test
gcloud auth configure-docker

## push to gcr ##
docker tag rembg:latest gcr.io/leaguecards-dev-test/rembg
docker push gcr.io/leaguecards-dev-test/rembg

Please note that leaguecards-dev-test is the project id

### Please create a service after this in console ###

Once done please copy the url returned by gcp console and store it in serverless.yml

suppose the path returned by gcp is https://something.com, the actual url which you have to 
save is https://something.com/test

Navigate to environment under serverless.yml and update the path .

### Serverless Deploy ###
This steps deploys AWS Config in your Account

### Install the sls framework for this step ###
npm install -g serverless
sls plugin install -n serverless-python-requirements

## Configure aws profile ##
download the security creds from the console, by going under your name> My Security Creds
aws configure --profile profilename

### export AWS PROFILE ##
export AWS_PROFILE=profilename

### Deploy ###
pip install -r requirements.txt
npm install -D serverless-layers
sls deploy --verbose

### rollback ###
sls remove

### Errors during remove or rollback ###
delete the stack from console

### IMPORTANT Step ###
Once the api gateway is deployed .
Navigate to the API, click settings . 
Goto binary media types and add */*.
 
Once done please redploy the api gateway for changes to take effect.
api gateway> click on prod rembg > actions >deploy api


