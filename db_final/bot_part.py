# 功能1爬取特定天數的天氣資訊並回傳
# 功能2使用不同的模型回傳預測結果
# 功能3取得當即時天氣結果


#調用 event 函式庫
#導入 Discord.py
import discord
from discord.ext import commands
import crawl_for_current_weather as cfcw
import joblib

# 載入模型
dctmodel = joblib.load("orig_dct.pkl")
knnmodel = joblib.load("orig_knn.pkl")

intents = discord.Intents.default()
intents.message_content = True
bot=commands.Bot(command_prefix='!', intents=intents) 

# 載入爬蟲
crawler = cfcw.crawl_weather()
tips = '''
輸入 !pcw 來用過去1小時的資料進行預測
輸入 !gcw 來獲得當前天氣
    '''

@bot.event
async def on_ready():
    print(">>bot is online<<")
@bot.command('helps')
async def hi(ctx):
    await ctx.send(tips)


# 獲得過去1小時的資料，並進行預測
@bot.command('pcw')
async def weather(ctx):
    await ctx.send("作業中")
    infos = crawler.return_info()
    time, temp, winds, pres = infos
    infos = [list(infos)]
    dct = dctmodel.predict(infos)
    knn = knnmodel.predict(infos)
    await ctx.send(f"Decision tree model預測降雨量為:{float(dct[0])}")
    await ctx.send(f"KNN model預測降雨量為:{float(knn[0])}")
    await ctx.send(f"現在時間{time}, 氣溫為{round(temp)}, 風速為{winds}, 壓力為{round(pres)}")
    await ctx.send("已完成")

# 獲得當前天氣
@bot.command('gcw')
async def cweather(ctx):
    await ctx.send("查詢中")
    infos = crawler.return_current_weathher()
    await ctx.send("目前室外天氣如下:")
    await ctx.send(f"目前的溫度為{infos[0].text}")
    await ctx.send(f'{infos[1]}\n{infos[2]}\n{infos[3]}')
    await ctx.send(tips)

# 如果要使用的話要把token改成自己的
# 可以基本設定和基礎的dicord bot相同
bot.run("MTA1NjIyMDExNjUyMzY4MzkyMQ.GBCcPJ.pAFYggdW0j07jY2NppejGdOhmi2ZnOiacdUpNI")
