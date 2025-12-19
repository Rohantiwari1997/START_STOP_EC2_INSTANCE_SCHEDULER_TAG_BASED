# EC2 Start/Stop Instance Scheduler (Tag-Based)

Automated EC2 instance scheduling using AWS Lambda and CloudWatch Events based on instance tags.

## Features

- **Tag-based scheduling**: Control instances using `AutoSchedule=true` tag
- **Flexible timing**: Configurable start/stop schedules via CloudWatch Events
- **Cost optimization**: Automatically stop instances during off-hours
- **Serverless**: Uses AWS Lambda for zero-maintenance operation

## Architecture

- **Lambda Function**: Handles start/stop logic
- **CloudWatch Events**: Triggers scheduled actions
- **IAM Roles**: Secure permissions for EC2 operations
- **CloudFormation**: Infrastructure as Code deployment

## Quick Start

### 1. Tag Your Instances
```bash
aws ec2 create-tags --resources i-1234567890abcdef0 --tags Key=AutoSchedule,Value=true
```

### 2. Deploy Infrastructure
```bash
aws cloudformation deploy \
  --template-file cloudformation.yaml \
  --stack-name ec2-scheduler \
  --capabilities CAPABILITY_IAM
```

### 3. Deploy Lambda Code
```bash
./deploy.sh
```

## Configuration

### Default Schedule
- **Start**: Monday-Friday at 10:00 AM UTC
- **Stop**: Tuesday-Saturday at 12:00 AM UTC  
- **Weekend Stop**: Saturday-Sunday at 9:00 AM UTC

### Required Tags
- `AutoSchedule=true` - Enables scheduling for the instance

## Files

- `lambda_function.py` - Main Lambda function
- `cloudformation.yaml` - AWS infrastructure template
- `deploy.sh` - Deployment script
- `requirements.txt` - Python dependencies
- `deployment-guide.md` - Detailed deployment instructions
- `tag-examples.md` - EC2 tagging examples

## Permissions

The Lambda function requires:
- `ec2:DescribeInstances`
- `ec2:StartInstances`
- `ec2:StopInstances`

## Monitoring

Check CloudWatch Logs for execution details:
```bash
aws logs describe-log-groups --log-group-name-prefix /aws/lambda/ec2-start-stop-scheduler
```

## License

MIT License - see LICENSE file for details.
