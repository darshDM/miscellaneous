import paramiko
import boto3
import json
from io import BytesIO
from stat import S_ISREF
from botocore.exceptions import ClientError

HOST = "[HOST(SFTP ADDRESS)]"
USERNAME = "[USERNAME]"
PASSWORD = "[PASSWORD]"
PORT = 22
s3_object = boto3.client("s3")
transport = paramiko.Transport((HOST, PORT))

def writeToS3(data,bucket,path):
	try:
		s3_object.upload_fileobj(data,bucket,path)
		print(f"File successfully uploaded to {bucket}")

	except:
		print("Something went wrong!!! couldn't connect to S3")

def lambda_handler(event, context):
    try:
        transport.connect(username=USERNAME, password=PASSWORD)
        with paramiko.SFTPClient.from_transport(transport) as sftp:
            try:
                # If you want change the current working directory
                sftp.chdir("important-files/games-n-stuff")
                all_files_folders = sftp.listdir_attr()
                for file in all_files_folders:
                    if S_ISREG(file.st_mode):
                        with BytesIO as data:
                            sftp.getfo(file.filename, data)
                            data.seek(0)
                            writeToS3(data, "[BUCKET_NAME]",f"{path}/{file.filename}")
            except IOError as e:
                print("input path doesn't exist")
    except paramiko.SSHExecption as e:
        print("oops! couldn't to SFTP")
