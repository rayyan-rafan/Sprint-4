import boto3
import time
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def log_to_cloudwatch(message, log_group, log_stream):
    try:
        client = boto3.client(
            'logs',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )

        try:
            client.create_log_group(logGroupName=log_group)
        except client.exceptions.ResourceAlreadyExistsException:
            pass

        try:
            client.create_log_stream(
                logGroupName=log_group,
                logStreamName=log_stream
            )
        except client.exceptions.ResourceAlreadyExistsException:
            pass

        return client.put_log_events(
            logGroupName=log_group,
            logStreamName=log_stream,
            logEvents=[
                {
                    'timestamp': int(time.time() * 1000),
                    'message': message
                }
            ]
        )

    except Exception as e:
        logger.error(f"Error logging to CloudWatch: {str(e)}")
        return None
