import boto3
import json
from datetime import datetime

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    
    # Get current day (0=Monday, 6=Sunday)
    current_day = datetime.now().weekday()
    
    # Weekend check (Saturday=5, Sunday=6)
    is_weekend = current_day >= 5
    
    # Get action from event or determine based on time
    action = event.get('action')
    if not action:
        current_hour = datetime.now().hour
        # Start at 10 AM, stop at midnight
        action = 'start' if 10 <= current_hour < 24 else 'stop'
    
    # Get instances with scheduling tags
    tag_filters = [
        {'Name': 'tag:AutoSchedule', 'Values': ['true', 'weekdays', 'weekends']},
        {'Name': 'instance-state-name', 'Values': ['running', 'stopped']}
    ]
    
    if event.get('instance_ids'):
        tag_filters.append({'Name': 'instance-id', 'Values': event['instance_ids']})
    
    instances = ec2.describe_instances(Filters=tag_filters)
    
    weekday_instances = []
    weekend_instances = []
    
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            schedule_tag = next((tag['Value'] for tag in instance.get('Tags', []) 
                               if tag['Key'] == 'AutoSchedule'), None)
            
            if schedule_tag == 'weekdays':
                weekday_instances.append(instance['InstanceId'])
            elif schedule_tag == 'weekends':
                weekend_instances.append(instance['InstanceId'])
            elif schedule_tag == 'true':
                weekday_instances.append(instance['InstanceId'])
    
    messages = []
    all_processed = []
    
    try:
        # Handle weekday instances (10 AM-midnight schedule)
        if weekday_instances:
            if action == 'start':
                ec2.start_instances(InstanceIds=weekday_instances)
                messages.append(f'Started {len(weekday_instances)} scheduled instances')
            else:
                ec2.stop_instances(InstanceIds=weekday_instances)
                messages.append(f'Stopped {len(weekday_instances)} scheduled instances')
            all_processed.extend(weekday_instances)
        
        # Handle weekend-stopped instances (24/7 weekdays, stopped weekends)
        if weekend_instances:
            if not is_weekend:
                ec2.start_instances(InstanceIds=weekend_instances)
                messages.append(f'Started {len(weekend_instances)} 24/7 weekday instances')
            else:
                ec2.stop_instances(InstanceIds=weekend_instances)
                messages.append(f'Stopped {len(weekend_instances)} weekend-stopped instances')
            all_processed.extend(weekend_instances)
        
        if not all_processed:
            return {'statusCode': 200, 'body': 'No instances found with AutoSchedule tag'}
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': '; '.join(messages),
                'instances': all_processed,
                'day': current_day,
                'is_weekend': is_weekend
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }