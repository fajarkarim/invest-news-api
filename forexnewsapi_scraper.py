import requests
import pandas as pd
import dags.scripts.cloud_storage as cloud_storage
import datetime

url = "https://forexnewsapi.com/demo/index"

payload = "token=demo&tickers=EUR-USD&_token=a3UXtjuntwwiyA4jeuqMoVlBZ67rJuu1TXER7DJb"
headers = {
    "cookie": "XSRF-TOKEN=eyJpdiI6InRUMmY5QWJzRzJmQlwvNDVoeXViYTJnPT0iLCJ2YWx1ZSI6ImplWmgrYnJvZEt2V3NhMktQSitxS0xCVUFOUXNkTVVrTGI1a2dyNEx2OFdhK1hXYjlJYm4wUlRiT1RienRsQTIiLCJtYWMiOiI4NzkyNTc2MTc5ZmFlYjE1NmE2ZDJjOWFiZDA2MWE1ZTUwNGMyYjNmNzMxN2IyY2YxZGVkMzMyMWYyMWNmMmQ1In0%253D; cryptonews_api_session=eyJpdiI6IkhUeVpUMFZodHl4QTlNd2FlZzg2TkE9PSIsInZhbHVlIjoidzl3VW45bzNwaEtac1BpSUE5TGVsZ0lzZkNiV3lBd3dCQ2F2N1pPenFKY2NVVFUybVYyWVVlZDBCYzhaWUdvMyIsIm1hYyI6Ijk1MTUyZjQ4MjMwNTM1ZDMwYjhjYzFkYzhmNzRmZDAzYzM5YTA0NjQ1MmJlODgwOTc4NmQ1NTE3M2Q3N2U4MGUifQ%253D%253D",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie": "_ga=GA1.2.760991717.1659535257; messagesUtk=a059ac94f8d34799a9138e0f5a777692; hubspotutk=eab726450e9ca26aa571ed027186f6b2; __stripe_mid=56afc2e9-60ed-4a46-b3c4-e648e1dc4281dd2e14; _gid=GA1.2.126899357.1662029295; _gat_gtag_UA_121402530_7=1; __hstc=123358612.eab726450e9ca26aa571ed027186f6b2.1659535261034.1660789135022.1662029306588.5; __hssrc=1; __hssc=123358612.4.1662029306588; XSRF-TOKEN=eyJpdiI6Ikx0bVc5MEtzckFlWlwvSjhxNkJBaUxRPT0iLCJ2YWx1ZSI6InpTUGFZK09XT2xMOGJGOFpEVXZWNFQ2OFNqVGVDZGl6SnFaY2tyTDA4aG1sWWkrVVM5ZXZzMENmektXdHZkQ2MiLCJtYWMiOiJiZjJjZjliODE0Mzk4NWQzM2E3MjVlODM2YTA0YWU5Nzg0OGQxNjVhYjM4MDJkZWYxYmZhOWVmOWFmOTY5ZTQ1In0%3D; cryptonews_api_session=eyJpdiI6Ik9EaWVJcUZMOTJnMFNNUWxpUHNYa3c9PSIsInZhbHVlIjoiYTRnOUR0bTlWR1hTRGFWa04wSTRyQ0t0WllPZG9kXC9aM05WU2JIUTdnS3ozTEpYcFFGS2NHQU1adEpnSkc4QnciLCJtYWMiOiJmZTZiYWM5NTc3YmI4NGU5NmRiNzJjMWY5YTZlZmZkNzAzNmI4MzJjNzY0MTQ4ODA3MmY5NDMzZjI4Y2QzZDU3In0%3D",
    "Origin": "https://forexnewsapi.com",
    "Referer": "https://forexnewsapi.com/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
    "sec-ch-ua": '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
    "sec-ch-ua-mobile": "?0"
}

response = requests.request("POST", url, data=payload, headers=headers).json()

data = response['data']
PAIR = "EUR-USD"

BUCKET_NAME = "baby-pips-calendar-news"
DATA_SOURCE = "forexnewsapi"
CURRENT_TIME =  datetime.datetime.now()
csvName = f"{DATA_SOURCE}_{PAIR}_{CURRENT_TIME.date()}.csv"


df = pd.json_normalize(data)

df.to_csv(csvName, index=False)

# cloud_storage.uploadFromString(BUCKET_NAME, df.to_csv(), csvName)