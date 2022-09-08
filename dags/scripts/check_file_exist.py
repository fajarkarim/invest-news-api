from google.cloud import storage

BUCKET_NAME = "baby-pips-calendar-news"
fileName = "coba.csv"

storageClient = storage.Client()
bucket = storageClient.bucket(BUCKET_NAME)
fileBlob = bucket.blob(fileName)
print(fileBlob.exists())
