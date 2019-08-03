import requests
import json
import os
from datetime import datetime
import time

"""
https://query1.finance.yahoo.com/v8/finance/chart/AAPL?symbol=AAPL&period1=0&period2=9999999999&interval=1d&includePrePost=true&events=div%2Csplit
https://stackoverflow.com/questions/44030983/yahoo-finance-url-not-working
"""

BASE_URL = "https://finance.yahoo.com/quote/{ID}/history?p={ID}"
QUERY_URL = "https://query1.finance.yahoo.com/v7/finance/download/{ID}?period1={PERIOD1}&period2={PERIOD2}&interval={INTERVAL}&events=history&crumb={CRUMB}"
QUERY_URL_TEST = "https://query1.finance.yahoo.com/v7/finance/download/{ID}?period1=1530721419&period2=1562257419&interval={INTERVAL}&events=history&crumb={CRUMB}"
COOKIE_KEY ="set-cookie"
COOKIE_FMT = "cookie:{}"
CRUMB_KEY = b"CrumbStore\":{\"crumb\":\""
CRUMB_KEY_STR = "CrumbStore"
CRUMB_KEY_STR_LOW = "crumb"
CRUMB_KEY_END = b"}"

TIME_FMT = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}"
COOKIE_TMP = "cookie.tmp"

class DateTimeConvertor(object):

    def fromTimeStamp(timestamp):
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

    def fromDate(timestr, fmt='%Y-%m-%d %H:%M:%S'):
        return int(time.mktime(datetime.strptime(timestr, fmt).timetuple()))

class YAHOOFINANCE(object):

    __slot__ = ("id", "crumb", "cookie", "fmt_txt", "interval", "p1", "p2")

    def __init__(self, interval="1d"):
        self.id = None
        self.crumb = None
        self.cookie = 'cookie:{}'
        self.fmt_txt = None
        self.interval = interval
        self.p1 = 0
        self.p2 = 0

    def set_id(self, id:str):
        self.id = id

    def get_cookie(self):
        url = BASE_URL.format(ID=self.id)
        req = requests.get(BASE_URL)
        res = req.headers
        print(res, req.content)
        self.cookie = res[COOKIE_KEY].split(";")[0][2:]
        self.fmt_txt = req.content
        print("Cookie:", self.cookie)
        a = yah.fmt_txt.find(b"CrumbStore\":{\"crumb\":\"")
        b = yah.fmt_txt[a:].find(CRUMB_KEY_END) + 1
        crumb_str = "{" + yah.fmt_txt[a-1:a+b].decode() + "}"
        print("Crumb:", crumb_str)
        self.crumb = json.loads(crumb_str)[CRUMB_KEY_STR][CRUMB_KEY_STR_LOW]
        print("Crumb:", self.crumb)
        
    def save_cookie(self):
        cookie = "{\"cookie\":{},\"crumb\":{}}\n".format(self.cookie,self.crumb)
        with open(COOKIE_TMP, "w") as f:
            f.write(cookie)
    
    def load_cookie(self):
        with open(COOKIE_TMP, "r") as f:
            cookie = f.read().split("\n")[0]
        loads = json.loads(cookie)
        self.cookie = loads["cookie"]
        self.crumb = loads["crumb"]
    
    def download_csv(self, quer_fmt=QUERY_URL_TEST, p1=None, p2=None, crumb=None, interval="1d"):
        if (p1 == None) or (p2 == None):
            if (self.p1 == 0) or (self.p2 == 0):
                self.p2 = int(time.now())
                self.p1 = p2 - 86400
        if (crumb == None) and (self.crumb == None):
            print("No crumb is collected!! Exit...")
            return
        else:
            self.crumb = crumb
        if self.interval == None:
            self.interval = interval

        query_url = quer_fmt.format(ID=self.id,
                                    PERIOD1=self.p1,
                                    PERIOD2=self.p2,
                                    INTERVAL=self.interval,
                                    CRUMB=self.crumb)
        # print(query_url)
        res = requests.get(query_url,cookies=self.cookie)
        return res

    def setPeriod(y1,m1,d1,y2,m2,d2):
        time_start = TIME_FMT.format(y1, m1, d1, 0, 0, 5)
        time_end = TIME_FMT.format(y2, m2, d2, 23, 55, 55)
        start = DateTimeConvertor.fromDate(time_start)
        end = DateTimeConvertor.fromDate(time_end)
        self.p1 = start
        self.p2 = end


import argparse

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", type=str, default="GOOG", help="symbol")
    parser.add_argument("-sd", type=str, help="start date fmt:{YYYY:MM:DD}")
    parser.add_argument("-ed", type=str, help="end date fmt:{YYYY:MM:DD}")

    return parser.parse_args()

def main():
    args = get_args()
    api = YAHOOFINANCE()
    api.set_id(args.s)
    api.get_cookie()
    api.save_cookie()
    res = api.download_csv().info()
    csv_file = "res.csv"
    with open(csv_file, "w") as f:
        f.write(res)



if __name__ == '__main__':
    main()