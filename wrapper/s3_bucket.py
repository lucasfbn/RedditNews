import json

import boto3
from botocore.client import Config


class S3Bucket:

    def __init__(self, bucket_name, bucket_access_key, bucket_access_secret):
        self.bucket_name = bucket_name
        self.bucket = self._auth(bucket_access_key, bucket_access_secret)

    @staticmethod
    def _auth(bucket_access_key, bucket_access_secret):
        return boto3.resource(
            's3',
            aws_access_key_id=bucket_access_key,
            aws_secret_access_key=bucket_access_secret,
            config=Config(signature_version='s3v4')
        )

    def upload(self, key, data):
        self.bucket.Bucket(self.bucket_name).put_object(Key=key, Body=data)

    def download(self, key):
        content = self.bucket.Object(self.bucket_name, key).get()['Body'].read()
        return json.loads(content)
