# EC2 Start/Stop Scheduler - Deployment Guide

## Prerequisites

- AWS CLI configured with appropriate permissions
- EC2 instances tagged with `AutoSchedule=true`

## Deployment Steps

### 1. Deploy Infrastructure
```bash
aws cloudformation deploy \
  --template-file cloudformation.yaml \
  --stack-name ec2-scheduler \
  --capabilities CAPABILITY_IAM
```

### 2. Package and Deploy Lambda Code
```bash
# Create deployment package
zip -r function.zip lambda_function.py

# Upload to Lambda
aws lambda update-function-code \
  --function-name ec2-start-stop-scheduler \
  --zip-file fileb://function.zip
```

### 3. Verify Deployment
```bash
# Test start function
aws lambda invoke \
  --function-name ec2-start-stop-scheduler \
  --payload '{"action": "start"}' \
  response.json

# Check response
cat response.json
```

## Required IAM Permissions

The Lambda function needs:
- `ec2:DescribeInstances`
- `ec2:StartInstances` 
- `ec2:StopInstances`

## Schedule Configuration

- **Start**: Monday-Friday at 10:00 AM UTC
- **Stop**: Tuesday-Saturday at 12:00 AM UTC
- **Weekend Stop**: Saturday-Sunday at 9:00 AM UTC

## Troubleshooting

- Check CloudWatch logs for Lambda execution details
- Verify EC2 instances have `AutoSchedule=true` tag
- Ensure Lambda has proper IAM permissions
