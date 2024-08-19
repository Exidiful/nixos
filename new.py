import boto3
from botocore.exceptions import ClientError

def get_s3_buckets_without_logging():
    s3 = boto3.client("s3")
    buckets_without_logging = []

    try:
        response = s3.list_buckets()
        buckets = response["Buckets"]

        for bucket in buckets:
            bucket_name = bucket["Name"]
            try:
                logging_status = s3.get_bucket_logging(Bucket=bucket_name)
                if "LoggingEnabled" not in logging_status:
                    buckets_without_logging.append(bucket_name)
            except ClientError as e:
                print(f"Error checking logging for {bucket_name}: {e.response['Error']['Message']}")

    except ClientError as e:
        print(f"An error occurred while listing buckets: {e.response['Error']['Message']}")

    return buckets_without_logging

def print_buckets_and_confirm(buckets):
    print("S3 buckets with access logging disabled:")
    for bucket in buckets:
        print(f"- {bucket}")
    
    confirmation = input("\nDo you want to enable access logging for these buckets? (yes/no): ").lower().strip()
    return confirmation == 'yes'

def enable_s3_bucket_logging(bucket_name, target_bucket, target_prefix):
    s3 = boto3.client("s3")
    try:
        s3.put_bucket_logging(
            Bucket=bucket_name,
            BucketLoggingStatus={
                'LoggingEnabled': {
                    'TargetBucket': target_bucket,
                    'TargetPrefix': f"{target_prefix}/{bucket_name}/"
                }
            }
        )
        print(f"Enabled logging for {bucket_name}")
    except ClientError as e:
        print(f"Error enabling logging for {bucket_name}: {e.response['Error']['Message']}")

if __name__ == "__main__":
    buckets_without_logging = get_s3_buckets_without_logging()
    
    if not buckets_without_logging:
        print("All buckets already have logging enabled.")
    else:
        if print_buckets_and_confirm(buckets_without_logging):
            print(f"\nEnabling logging for {len(buckets_without_logging)} buckets:")
            target_bucket = "xxx-global-dev-logs"
            target_prefix = "s3-access-logs"
            for bucket in buckets_without_logging:
                enable_s3_bucket_logging(bucket, target_bucket, target_prefix)
        else:
            print("Operation cancelled. No changes were made.")
