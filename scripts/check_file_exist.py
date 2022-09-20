from fileinput import filename
import sys
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/root/gcloud_credential/stoked-brand-360411-bc40ff939c35.json"
from google.cloud import storage

def checkFile(**kwargs):
    BUCKET_NAME = "baby-pips-calendar-news"
    fileName = kwargs["fileName"]

    storageClient = storage.Client()
    bucket = storageClient.bucket(BUCKET_NAME)
    isFileBlobExist = bucket.blob(fileName).exists(storageClient)

    if (not isFileBlobExist):
        raise ValueError(f"{fileName} doesn't exist")

if __name__ == "__main__":
    checkFile(fileName=sys.argv[1])