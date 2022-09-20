import requests
import pandas as pd
import sys
from fajar.invest_news_api.cloud_storage import uploadFromString
import os
from datetime import datetime

def getNextWeekParam(currentDate):
    currentTime = datetime.strptime(currentDate, "%Y-%m-%d")
    year, week_num, day = currentTime.isocalendar()
    nextWeek = week_num + 1
    nextWeekParam = f"{year}-W{nextWeek}"
    return nextWeekParam

def scrape(**context):

    nextWeekParam = context["nextWeekParam"]
    url = "https://www.babypips.com/economic-calendar"
    querystring = {"week": nextWeekParam}

    headers = {
        "authority": "www.babypips.com",
        "accept": "application/json",
        "accept-language": "en-US,en;q=0.9",
        "cookie": "_fbp=fb.1.1658917317280.1043771616; __gads=ID=6220a4c542d2c71e:T=1658917318:S=ALNI_MZfSKXYNECNvhl7daOWj4CFBRCugw; _hjSessionUser_66086=eyJpZCI6IjAyMzAyNWI5LTEyZDMtNWE5OC1iNTU1LTQ1N2MxNmJjMjE1MSIsImNyZWF0ZWQiOjE2NTg5MTczMTcyNjksImV4aXN0aW5nIjp0cnVlfQ==; _jsuid=1434589699; _referrer_og=https%3A%2F%2Fwww.google.com%2F; __qca=P0-1881981861-1659799278380; _hp2_id.264507251=%7B%22userId%22%3A%224048609373992413%22%2C%22pageviewId%22%3A%227650184054813523%22%2C%22sessionId%22%3A%224883787769421579%22%2C%22identity%22%3Anull%2C%22trackerVersion%22%3A%224.0%22%7D; _gid=GA1.2.1652517592.1660998553; _hjSession_66086=eyJpZCI6IjRmYzljYjRhLWEwZmEtNGViOS04YWJhLTNjYTg1ZDBlYzMwZSIsImNyZWF0ZWQiOjE2NjEwNjU4NzUwMzUsImluU2FtcGxlIjp0cnVlfQ==; _hjAbsoluteSessionInProgress=0; __gpi=UID=0000081aa616a639:T=1658917318:RT=1661065876:S=ALNI_MbDKKlwfzvG31Bqn72FsaLQvbyZ2Q; _hjIncludedInSessionSample=1; dt=Sun Aug 21 2022; _hjIncludedInPageviewSample=1; bp_calendar_filters=%7B%7D; _ga_Q22H2M47P8=GS1.1.1661065874.19.1.1661069156.0.0.0; OptanonAlertBoxClosed=2022-08-21T08:05:56.949Z; _ga=GA1.2.1984377348.1658917316; OptanonConsent=isIABGlobal=false&datestamp=Sun+Aug+21+2022+15%3A05%3A57+GMT%2B0700+(Western+Indonesia+Time)&version=6.24.0&hosts=&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0002%3A1%2CSPD_BG%3A1%2CC0004%3A1&AwaitingReconsent=false&geolocation=ID%3BJK; _first_pageview=1",
        "if-none-match": "ff835b6aee5dca40599a19606bc8b363",
        "referer": "https://www.babypips.com/economic-calendar?week=2022-W33",
        "sec-ch-ua": '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "macOS",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
    }

    response = requests.request("GET", url, headers=headers, params=querystring).json()
    events = response["events"]
    week = response["filters"]["week"]
    WEB_SOURCE = "babypips.com"
    BUCKET_NAME = "baby-pips-calendar-news"
    csvName = f"{WEB_SOURCE}_{week}.csv"

    tmp = []

    for news in events:
        tmp.append(news) 

    df = pd.json_normalize(tmp)

    uploadFromString(BUCKET_NAME, df.to_csv(), csvName)

    return csvName

if __name__ == "__main__":
    scrape(nextWeekParam=sys.argv[1])


