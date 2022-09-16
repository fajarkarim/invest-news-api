from fileinput import filename
import sys
# from google.cloud import storage

BUCKET_NAME = "baby-pips-calendar-news"
fileName = f"babypips.com_{sys.argv[1]}"

print(f"nama file nya --------- {fileName}")

# storageClient = storage.Client()
# bucket = storageClient.bucket(BUCKET_NAME)
# fileBlob = bucket.blob(fileName)

# if (not fileBlob):
#     raise ValueError(f"{fileName} doesn't exist")
