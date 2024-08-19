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
        print(f"Enabling logging for {len(buckets_without_logging)} buckets:")
        for bucket in buckets_without_logging:
            # You may want to customize these values
            target_bucket = bucket  # Using the same bucket as the target
            target_prefix = "logs"
            enable_s3_bucket_logging(bucket, target_bucket, target_prefix)
from botocore.exceptions import ClientError


def get_s3_buckets_logging_status():
    # Create an S3 client
    s3 = boto3.client("s3")

    try:
        # Get list of all buckets
        response = s3.list_buckets()
        buckets = response["Buckets"]

        print("S3 Buckets and their Server Access Logging Status:")
        print("------------------------------------------------")

        for bucket in buckets:
            bucket_name = bucket["Name"]
            try:
                # Get bucket logging configuration
                logging_status = s3.get_bucket_logging(Bucket=bucket_name)

                if "LoggingEnabled" in logging_status:
                    status = "Enabled"
                    target_bucket = logging_status["LoggingEnabled"]["TargetBucket"]
                    target_prefix = logging_status["LoggingEnabled"]["TargetPrefix"]
                    print(f"{bucket_name}: {status}")
                    print(f"  Target Bucket: {target_bucket}")
                    print(f"  Target Prefix: {target_prefix}")
                else:
                    status = "Disabled"
                    print(f"{bucket_name}: {status}")

                print("------------------------------------------------")

            except ClientError as e:
                print(f"{bucket_name}: Error - {e.response['Error']['Message']}")
                print("------------------------------------------------")

    except ClientError as e:
        print(f"An error occurred: {e.response['Error']['Message']}")


if __name__ == "__main__":
    get_s3_buckets_logging_status()
