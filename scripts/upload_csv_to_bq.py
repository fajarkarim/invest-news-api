from google.cloud import bigquery
import sys
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/root/gcloud_credential/stoked-brand-360411-bc40ff939c35.json"

def uploadCsv(**kwargs):
    try:
        csvFileName = kwargs["csvName"]
        TABLE_NAME = "COBA_AJA"
        client = bigquery.Client()

        TABLE_ID = f"stoked-brand-360411.web_scraping.{TABLE_NAME}"

        job_config = bigquery.LoadJobConfig(
            autodetect=True,
            skip_leading_rows=1,
            allow_quoted_newlines=True,
            source_format=bigquery.SourceFormat.CSV,
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE
        )

        uri = f"gs://baby-pips-calendar-news/{csvFileName}"

        load_job = client.load_table_from_uri(
            uri, TABLE_ID, job_config=job_config
        )  # Make an API request.

        load_job.result()

        destination_table = client.get_table(TABLE_ID)
        print("Loaded {} rows.".format(destination_table.num_rows))
        return True
    except:
        return False    

if __name__ == "__main__":
    uploadCsv(csvName=sys.argv[1])