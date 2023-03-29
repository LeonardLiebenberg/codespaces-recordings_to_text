import boto3,os

class UploadToS3:
    def __init__(self,aws_access_key,aws_secret_key,aws_session_token,region_name):
        self.aws_access_key = aws_access_key
        self.aws_secret_key = aws_secret_key
        self.aws_session_token = aws_session_token
        self.region_name = region_name

    def upload_to_s3(self,local_path,s3_prefix,bucket_name):
        s3 = boto3.client("s3", aws_access_key_id=self.aws_access_key, aws_secret_access_key=self.aws_secret_key,
                        aws_session_token=self.aws_session_token,region_name=self.region_name)
              
        local_folder = local_path
        file_names = os.listdir(local_folder)

        for file_name in file_names:
            file_path = os.path.join(local_folder, file_name)
            print(file_path)
            key = os.path.join(s3_prefix, file_name)
            print(key)
            s3.upload_file(file_path, bucket_name, s3_prefix +"/" + file_name)




# UploadToS3().upload_to_s3()




