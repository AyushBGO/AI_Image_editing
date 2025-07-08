import boto3
from botocore.exceptions import NoCredentialsError
import uuid
import os

# === AWS Configuration ===
AWS_ACCESS_KEY = "AKIA5DE6DN3A6324EUNL"
AWS_SECRET_KEY = "7HJxxP4U1fja8m3oB+lMWC/ZaBY/+Ru/hkVTm46E"
AWS_REGION = "us-east-1"  # e.g., "ap-south-1"
BUCKET_NAME = "wd-active-users"

# Initialize S3 client
s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

def upload_to_s3(file_path, folder):
    file_key = f"{folder}/{uuid.uuid4().hex}_{os.path.basename(file_path)}"
    try:
        s3.upload_file(file_path, BUCKET_NAME, file_key)
        return f"s3://{BUCKET_NAME}/{file_key}"
    except NoCredentialsError as e:
        print("❌ AWS Credentials not found or invalid.")
        return None
    except Exception as ex:
        print(f"❌ Upload failed: {ex}")
        return None


# 's3' => [
#             'driver' => 's3',
#             'key' => 'AKIA5DE6DN3A6324EUNL',
#             'secret' => '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',
#             'region' => 'us-east-1',
#             'bucket' => 'wd-active-users',
#         ],