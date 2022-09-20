
deploy:
	cp ./dags/babypips_calendar.py /root/airflow/dags/
	cp -r ./scripts/* /root/airflow/plugins/fajar/invest_news_api/
	cp -r ./analytics /root/airflow/dags/transform/