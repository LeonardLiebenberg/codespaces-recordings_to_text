# Callbi Recordings Uploader. Speech-To_Text

This app extracts .ogg call recordings from an SFTP, creates a csv file containing metadata for the call recordings, uploads the call recordings and the metadata file to an S3 bucket which triggers Callbi to download the dat afrom s3 and transcribe the recordings.

# Running audio uploader

Add your credentials to the docs/config.ini file

Run from main.py file using py -m main







