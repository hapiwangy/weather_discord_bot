from bs4 import BeautifulSoup
import concurrent.futures
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime, time

# global information
# 目前先假定"降水量", "紫外線指數", "日照時數"是要預測的目標
dicts = ["時間", "海平面氣壓", "氣溫", "風速", "降水量"] # 要記錄的標題
# 台北
station = [466920]
altitude = [5.3]
bm = [1,3,5,7,8,10]
sm = [4,6,9,11]
datas = []



def crawl_for_one(url):
    print(f"爬蟲進行中請稍後")
    response = requests.get(url)
    response.encoding="utf-8"
    content = BeautifulSoup(response.text, "html.parser")
    # 每個element都包含dicts所對應的資料

    # 把已經獲得的某測站/某天的資料作紀錄
    content = content.find("table", {"id":"MyTable"})
    content = content.find_all("tr")[3:]
    content = [x.find_all("td") for x in content]
    for con in content:
        result = [con[0],con[2],con[3],con[6],con[10]]
        datas.append([y.text.replace("\xa0", "") for y in result])




def main():
    stat_choice = 0
    enddate = '2022-11-30'
    enddate = datetime.datetime.strptime(enddate, "%Y-%m-%d")
    dates = datetime.datetime.strptime("2000-01-01", "%Y-%m-%d")
    t = time.time()
    urls = []
    while dates <= enddate:
        dt = dates.strftime("%Y-%m-%d")
        # print(dt.replace("-",""))
        dates += datetime.timedelta(1)
        url = r"https://e-service.cwb.gov.tw/HistoryDataQuery/DayDataController.do?command=viewMain&station="+str(station[int(stat_choice)])+"&stname=%25E7%25AB%25B9%25E5%25AD%2590%25E6%25B9%2596&datepicker="+str(dt)+"&altitude="+str(altitude[int(stat_choice)])+"m"
        urls.append(url)
    # 如果沒用threading的方式進行加速的話使用下面這個部分
    # for url in urls:
    #     crawl_for_one(url)
    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        executor.map(crawl_for_one, urls)
    # 把資料存成xlsx檔案方便之後訓練的時候做使用
    df = pd.DataFrame(datas, columns=dicts)
    df.to_excel(f"training_data_set.xlsx", index=False)
    print(f"共花費{time.time()-t}秒")
        
if __name__ == '__main__':
    main()
