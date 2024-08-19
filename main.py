import boto3
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
