Deployment Steps Order Wise

## docker build ##
docker build -t rembg .

## gcp auth ##
gcloud auth login
gcloud config set project leaguecards-dev-test
gcloud auth configure-docker

## Push to gcr ##
docker tag rembg:latest gcr.io/leaguecards-dev-test/rembg
docker push gcr.io/leaguecards-dev-test/rembg

Please note that leaguecards-dev-test is the project id

### Create a service after this in console ###
go to cloud run
click on create service
select the image which u have uploaded in the previous step
give the service name
select the region
select CPU is only allocated while processing
click on advanced settings
For Container port give 5000
For Capacity give 2GB RAM and 4vCPU
For execution env choose 2nd Gen 
Select allow all traffic/requests even the unauthorized ones

### Changing the serverless.yml ###

Once done please copy the url returned by gcp console for the service and store it in serverless.yml.
suppose the path returned by gcp is https://something.com, the actual url which you have to 
save is https://something.com/test

Navigate to environment under serverless.yml and update the path of gcp_url.

### Serverless Deploy ###
This steps deploys AWS Config in your Account
please change directory to other folder in this directory

### Install the sls framework for this step ###
npm install -g serverless
sls plugin install -n serverless-python-requirements

## Configure aws profile ##
download the security creds from the console, by going under your name> My Security Creds
aws configure --profile profilename

### Export AWS PROFILE ##
export AWS_PROFILE=profilename

### Deploy ###
pip install -r requirements.txt
npm install -D serverless-layers

If this is first time deploy or if it gives layer error then run 
sls deploy -c layer.yml 

finally
sls deploy --verbose

### Rollback ###
sls remove

### Errors during remove or rollback ###
delete the stack from console

### IMPORTANT Step ###
Once the api gateway is deployed .
Navigate to the API, click settings . 
Goto binary media types and add */*.
 
Once done please redploy the api gateway for changes to take effect.
api gateway> click on prod rembg > actions > deploy api


