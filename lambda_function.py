import os
import boto3
import botocore.config
import json
import subprocess


def lambda_handler(event, context):
  """
  Create a backup of an RDS MySQL database and store it on S3
  :param event: provides information about the triggering of the function
  :param context: provides information about the execution environment
  :return: True when successful
  """

  # Set the path to the executable scripts in the AWS Lambda environment.
  # Source: https://aws.amazon.com/blogs/compute/running-executables-in-aws-lambda/
  os.environ['PATH'] = os.environ['PATH'] + ':' + os.environ['LAMBDA_TASK_ROOT']

  database = os.environ['DATABASE']
  bucket = os.environ['BUCKET_BACKUP']
  secret_manager = os.environ['SECRET_MANAGER']

  secretsmanager = boto3.client('secretsmanager')
  response = secretsmanager.get_secret_value(SecretId=secret_manager)
  secret_string = response.get("SecretString")
  secret_dict = json.loads(secret_string)

  username = secret_dict.get("username")
  password = secret_dict.get("password")
  host = secret_dict.get("host")  

  # To execute the bash script on AWS Lambda, change its pemissions and move it into the /tmp/ directory.
  # Source: https://stackoverflow.com/a/48196444
  subprocess.check_call(["cp ./backup.sh /tmp/backup.sh && chmod 755 /tmp/backup.sh"], shell=True)

  subprocess.check_call(["/tmp/backup.sh", database, host, username, password], shell=True)

  # By default, S3 resolves buckets using the internet.  To use the VPC endpoint instead, use the 'path' addressing
  # style config.  Source: https://stackoverflow.com/a/44478894
  s3 = boto3.resource('s3')

  s3.meta.client.upload_file('/tmp/backup.sql', f'{bucket}', 'backup.sql')

  return True
