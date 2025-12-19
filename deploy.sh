#!/bin/bash

# Deploy EC2 Start/Stop Scheduler

echo "Deploying CloudFormation stack..."
aws cloudformation deploy \
  --template-file cloudformation.yaml \
  --stack-name ec2-scheduler \
  --capabilities CAPABILITY_IAM

echo "Packaging Lambda function..."
zip -r function.zip lambda_function.py

echo "Updating Lambda function code..."
aws lambda update-function-code \
  --function-name ec2-start-stop-scheduler \
  --zip-file fileb://function.zip

echo "Deployment complete!"
echo "Don't forget to tag your EC2 instances with AutoSchedule=true"