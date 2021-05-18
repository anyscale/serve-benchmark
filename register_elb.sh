# This script list the instances associated with an anyscale session, and register them to the load balancer target group.

# CHANGE THESE
ANYSCALE_SESSION_ID=ses_6pUGUV3YT10qy1vKHQtOo0
AWS_ELB_TARGET_GROUP_ARN=arn:aws:elasticloadbalancing:us-west-2:959243851260:targetgroup/serve-scalability-benchmark/0e7db9152bf6b1a6

aws ec2 describe-instances \
    --filter Name=tag-value,Values=$ANYSCALE_SESSION_ID \
    | jq '.Reservations[] | .Instances[] | select(.State.Name == "running") | .InstanceId | {"Id": ., "Port": 8000}'  \
    | jq -s "{\"Targets\": ., \"TargetGroupArn\": \"$AWS_ELB_TARGET_GROUP_ARN\"}" \
    > /tmp/target_group.json

aws elbv2 register-targets --cli-input-json "$(cat /tmp/target_group.json)"