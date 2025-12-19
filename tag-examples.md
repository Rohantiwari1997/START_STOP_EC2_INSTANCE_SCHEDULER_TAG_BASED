# Tag-Based Instance Scheduling

## Supported Tags

Tag your EC2 instances with `AutoSchedule` key and one of these values:

### Tag Values
- `AutoSchedule=true` - All 7 days: 10 AM-midnight schedule
- `AutoSchedule=weekdays` - Only runs Monday-Friday 10 AM-midnight
- `AutoSchedule=weekends` - Runs weekdays 24/7, stopped on weekends

## Behavior Examples

**`AutoSchedule=weekdays`**
- Monday-Friday: Start 10 AM, stop midnight
- Saturday-Sunday: Always stopped

**`AutoSchedule=weekends`** 
- Monday-Friday: Running 24/7 (always on)
- Saturday-Sunday: Always stopped

**`AutoSchedule=true`**
- All 7 days: Start 10 AM, stop midnight
- No days off (runs every day with schedule) (same as weekdays)

## AWS CLI Examples

```bash
# Weekday-only instances
aws ec2 create-tags \
  --resources i-1234567890abcdef0 \
  --tags Key=AutoSchedule,Value=weekdays

# Weekend-only instances  
aws ec2 create-tags \
  --resources i-0987654321fedcba0 \
  --tags Key=AutoSchedule,Value=weekends

# Standard schedule (weekdays + weekend off)
aws ec2 create-tags \
  --resources i-1111222233334444 \
  --tags Key=AutoSchedule,Value=true
```