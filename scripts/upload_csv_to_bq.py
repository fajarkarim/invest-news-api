from google.cloud import bigquery

client = bigquery.Client()

TABLE_ID = "stoked-brand-360411.web_scraping.coba_2"

job_config = bigquery.LoadJobConfig(
    autodetect=True,
    skip_leading_rows=1,
    allow_quoted_newlines=True,
    source_format=bigquery.SourceFormat.CSV,
    write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE
)

uri = "gs://baby-pips-calendar-news/babypips.com_2022-W33.csv"

load_job = client.load_table_from_uri(
    uri, TABLE_ID, job_config=job_config
)  # Make an API request.

load_job.result()

destination_table = client.get_table(TABLE_ID)
print("Loaded {} rows.".format(destination_table.num_rows))

