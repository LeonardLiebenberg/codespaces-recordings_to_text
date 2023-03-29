from file_manager import FilePathManager,SFTPFileManager
from connector import SFTP,PostgresDatabase,CallbiAPI
from metadata import Metadata
from validation import ValidateMetaFiles,ValidateUpload
from conf import CallbiConfig
from api_data import ApiData
from s3_upload import UploadToS3
from validation import ValidateUpload


def main():

    """
    Downloads audio files from an sftp and stores them in a local directory
    """

    # #Establish connection to sftp
    sftp = SFTP().connect()
    local_pm = FilePathManager('C:/Users/LeonardLiebenberg/Documents/BestForU/Collections/SpeechToText/UploadRecordings/sttUploadAudio/src')

    # # #Set SFTP root directory
    sftp_pm = SFTPFileManager(sftp,"/")
    # # #Navigate to latest directory on sftp
    # remote_path = '/20230320'
    remote_path = sftp_pm.newest_dir()
    # # #Instantiate local directory
    # # #Navigate to directory you want to save audio files
    local_path = local_pm.navigate("../assets/Recordings")
    # # #download audio files from sftp
    sftp_pm.download_recordings(remote_path,local_path)

    """
    Create a metadata file
    """
    
    #Instantiate classes
    meta = Metadata()
    pgengine = PostgresDatabase().connect()

    # # #create recordings dataframe
    rdf = meta.get_recording_dataframe(local_path)
    # print(rdf.info())
    # # #create call data frame from postgre 
    cdf = meta.get_call_dataframe(pgengine,local_path)
    # # print(cdf.info())
    # # #create metadata file by merging recordings and calls info
    mdf = meta.create_metadata_file(rdf,cdf)
    # # #save metadata file to recordings directory
    mdf.to_csv(local_path + "/metadata.csv",index = False)

    """
    Validate Recordings match metadata file
    """
    # Create lists containing audio file names
    audio_file_names = rdf.AudioFileName.to_list()
    # # print(audio_file_names)
    metadata_audio_file_names = mdf.AudioFileName.to_list()
    # # print(metadata_audio_file_names)

    # # #instantiate validation class
    validate = ValidateMetaFiles(audio_file_names,metadata_audio_file_names)
    # # # get recording audio file names that are missing from the metadata file
    missing_audio_files = validate.list_missmatch()
    # # print(missing_audio_files)

    # # # remove the missing audio files from recordings
    local_pm.remove_files(missing_audio_files,local_path)

    """
    Create an upload on Callbi
    """

    # Create an upload
    # 
    config = CallbiConfig()
    callbi = CallbiAPI(config)
    data = ApiData()

    response = callbi.post("/api/v2019-07-08/organizations/{}/uploads",config.organization_key)
    upload_data = data.upload_data(response)

    # Get S3 temporary credentials from callbi api

    response = callbi.post("/api/v2019-07-08/organizations/{}/uploads/{}/credentials",config.organization_key,upload_data['uploadId'])
    credentials = data.s3_credentials(response)

    # #Upload files to s3 bucket 

    s3_client = UploadToS3(credentials['awsAccessKey'],credentials['awsSecretKey'],credentials['awsSessionToken'],upload_data['s3Region'])
    s3_client.upload_to_s3(local_path,upload_data['s3KeyPrefix'],upload_data['s3BucketName'])

    # #Mark upload as complete

    callbi.put("/api/v2019-07-08/organizations/{}/uploads/{}",config.organization_key,upload_data['uploadId'])

    # #Get import id

    organization_key = 205
    upload_data = 182202

    response = callbi.get("/api/v2019-07-08/organizations/{}/uploads/{}/imports",config.organization_key,upload_data['uploadId'])
    import_data = data.import_data(response)
    
    response = callbi.get("/api/v2019-07-08/organizations/{}/uploads/{}/imports",organization_key,upload_data)
    import_data = data.import_data(response)

    # #Get all import entries

    validate_upload = ValidateUpload("/api/v2019-07-08/organizations/{}/imports/{}/status".format(config.organization_key,import_data['importId']))
    validate_upload.check_import_status()

    validate_upload = ValidateUpload("/api/v2019-07-08/organizations/{}/imports/{}/status".format('205','179977'))
    validate_upload.check_import_status()

    files = local_pm.list_files("../assets/Recordings")
    local_pm.remove_files(files,local_path)
    

if __name__ == "__main__":
    main()