
from google.cloud import storage

storage_client = storage.Client()

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        f"File {source_file_name} uploaded to {destination_blob_name}."
    )


def uploadFromString(bucketName, contents, targetName):
    bucket = storage_client.bucket(bucketName)
    blob = bucket.blob(targetName)
    blob.upload_from_string(contents, 'text/csv')
    print(f"{targetName} has been upload to {bucketName}")