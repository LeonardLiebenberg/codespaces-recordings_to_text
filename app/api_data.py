import html
class ApiData:
    def __init__(self):
        self.data = {}
        self.upload_info = {}
        self.credentials = {}
        self.import_info = {}

    def upload_data(self,response):
        if response.status_code == 200:
            self.data = response.json()
            self.upload_info['uploadId'] = self.data['uploadId']
            self.upload_info['s3Region'] = self.data['s3Region']
            self.upload_info['s3BucketName'] = self.data['s3BucketName']
            self.upload_info['s3KeyPrefix'] = self.data['s3KeyPrefix']

            return self.upload_info
        
    def s3_credentials(self, response):
        if response.status_code == 200:
            self.data = response.json()

            session_access_str = str(self.data['awsAccessKey'])
            decoded_access_token = html.unescape(session_access_str)
            self.credentials['awsAccessKey'] = decoded_access_token

            session_secret_str = str(self.data['awsSecretKey'])
            decoded_secret_token = html.unescape(session_secret_str)
            self.credentials['awsSecretKey'] = decoded_secret_token

            session_token_str = str(self.data['awsSessionToken'])
            decoded_session_token = html.unescape(session_token_str)
            self.credentials['awsSessionToken'] = decoded_session_token

            return self.credentials
    
    def import_data(self,response):
        if response.status_code == 200:
            self.data = response.json()
            self.import_info['importId'] = self.data['items'][0]['id']
            return self.import_info
        

        
        
    



