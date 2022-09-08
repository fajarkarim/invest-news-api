# invest-news-api
Simple forex news extractor from web page to api using dbt as transforming and testing tools

## Diagram flow
Here is simple diagram flow of the system. I using cloud storage to store scraping result in csv format then put it to bigquery database. After that using dbt to transform and test the data.

![diagram](https://i.postimg.cc/xjZnJxb0/Screen-Shot-2022-09-09-at-00-02-21.png)


Airflow DAG

![Airflow dag](https://i.postimg.cc/xCPNjG4r/Screen-Shot-2022-09-08-at-23-14-30.png)


