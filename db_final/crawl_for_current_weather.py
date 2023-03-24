import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class crawl_weather:
    def __init__(self):
        # 定義瀏覽器的相關資訊
        self.option = Options()
        self.option.add_argument("--headless")
        self.driver = webdriver.Chrome(r"C:\Users\ASUS\Desktop\final_project\db_final_proj\chromedriver.exe", options=self.option)
        # 專注在台北就好了
        self.url = f"https://www.cwb.gov.tw/V8/C/W/OBS_Station.html?ID=46692"
        # 定義風力和級數的轉換
        self.wind_trans = {1:0.75, 2:2.5,3:4.4, 4:6.7, 5:9.35, 6:11.3, 7:16}
    # 爬取天氣之類的資訊
    def get_weather(self):
        self.driver.get(self.url)
        self.context = self.driver.page_source
        self.driver.quit()
        self.context = BeautifulSoup(self.context, "html.parser")
        self.context = self.context.find("div",{"class":"wrapper"})
        self.context = self.context.find("tbody")
        self.context = self.context.find_all("tr")
    # 回傳所有需要的資訊
    def return_info(self):
        self.get_weather()
        time = self.context[0].find("th").text.split(" ")[1][:2]
        temps = 0
        winds = 0
        pres = 0
        for x in self.context[:8]:
            temp = x.find("td",{"headers":"temp"})
            temp = temp.find("span", {"class":"tem-C is-active"})
            wind = x.find("span",{"class":"wind_1 is-active"})
            pre = x.find("td", {"headers":"pre"})
            pres += float(pre.text)
            winds += int(wind.text)
            temps += float(temp.text)
        temps = temps / 7
        winds /= 7
        pres /= 7
        return int(time), temps, self.wind_trans.get(int(winds), 30), pres
    # 獲得當前所有的資訊
    def return_current_weathher(self):
        url = r"https://www.google.com/search?q=%E5%8F%8A%E6%99%82%E5%A4%A9%E6%B0%A3%E7%8D%B2%E5%8F%96&rlz=1C1ONGR_zh-TWTW1012TW1012&oq=%E5%8F%8A%E6%99%82%E5%A4%A9%E6%B0%A3%E7%8D%B2%E5%8F%96&aqs=chrome.0.69i59j0i546l5.2915j1j7&sourceid=chrome&ie=UTF-8"
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.option)
        driver.get(url)
        content = driver.page_source
        driver.quit()
        content = BeautifulSoup(content, "html.parser")
        content = content.find("body")
        content = content.find("div", {"class":"main"})
        content = content.find("div", {"class":"eqAnXb"})
        content = content.find("div", {"class":"UQt4rd"})
        temp = content.find("div", {"class":"vk_bk TylWce SGNhVe"})
        temp = temp.find("span", {"class":"wob_t q8U8x"})
        infos = content.find("div", {"class":"wtsRwe"})
        infos = infos.find_all("div")
        rain_rate, humidity, winds = infos[0].text, infos[1].text, infos[2].text
        return temp, rain_rate, humidity, winds
# print(context[0])
# 把最近一個小時的平均資料丟進模型進行判斷，最後來得到模型的輸出
# time, temp, wind, 海平面氣壓

# time_part
# time = context[0].find("th").text.split(" ")[1][:2]
# print(time)

# temp_part
# temps = 0
# for x in context[:8]:
#     temp = x.find("td",{"headers":"temp"})
#     temp = temp.find("span", {"class":"tem-C is-active"})
#     temps += float(temp.text)
# temps = temps / 7
# print(temps)

# # winds_part
# winds = 0
# for x in context[:8]:
#     wind = x.find("span",{"class":"wind_1 is-active"})
#     winds += int(wind.text)
# winds /= 7
# print(winds)

# # pressure_part
# pres = 0
# for x in context[:8]:
#     pre = x.find("td", {"headers":"pre"})
#     pres += float(pre.text)
# pres /= 7
# print(pres)
