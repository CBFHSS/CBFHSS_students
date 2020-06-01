from django.conf import settings

from linebot import LineBotApi
from linebot.models import TextSendMessage, ImageSendMessage, StickerSendMessage, LocationSendMessage, QuickReply, QuickReplyButton, MessageAction
from googlesheet import googlesheettest
import datetime
from datetime import date
import time
import calendar
import gspread
import mysql.connector
from oauth2client.service_account import ServiceAccountCredentials
from module import todatabase
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)

def fix(event): #系統
    reply="系統維護中"
    try:
        message = TextSendMessage(  
            text = reply
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
def unauthorize(event):#沒權限
    try:
        message = TextSendMessage(  
            text = "您沒有新增及刪除的權限"
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
def manual(event): #功能簡介
    reply="請開啟選單開始使用本系統\n\n"
    reply+="使用方法\n"
    reply+="https://hackmd.io/TOAK5TdJSS-4Un4BuO2T2w\n"
    reply+="版本紀錄\n"
    reply+="https://hackmd.io/YvYW8hDkSwG3ZDgm1p0VRg\n"
    reply+="本程式官方網站\n"
    reply+="http://cbfhss.nctu.me/\n"
    reply+="錯誤回報&給予建議\n"
    reply+="https://forms.gle/ynVoyBhhJNyvypP9A\n"
    try:
        message = TextSendMessage(  
            text = reply
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
def addhwsuccess(event): #新增作業成功
    try:
        message = TextSendMessage(  
            text = "新增作業成功"
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
def addtemperturesuccess(event): #新增體溫成功
    try:
        message = TextSendMessage(  
            text = "新增體溫成功"
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
def hwreply(event): #顯示作業
    timeotp=time.strftime("%Y/%m/%d", time.localtime())
    pr=timeotp+" 功課：\n\n--------------------\n\n"
    pr+=googlesheettest.homework()
    pr+="\n--------------------\n\n(o｀з’*)୨📃"
    try:
        message = TextSendMessage(  
            text = pr
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
def seetemperture(event): #顯示體溫
    lssh1 = mysql.connector.connect(
    host = todatabase.host(),
    port = "3306",
    user = todatabase.username(),
    password = todatabase.password(),
    database = todatabase.database(),)
    gcpsql= lssh1.cursor()
    userid=event.source.user_id
    user_id="""select * from user_id"""
    gcpsql.execute(user_id)
    records = gcpsql.fetchall()
    timeotp=time.strftime("%Y/%m/%d", time.localtime())
    pr=timeotp
    for row in records:
        if row[3] == str(userid):
            pr+=googlesheettest.temperture(int(row[1]))
    try:
        message = TextSendMessage(  
            text = pr
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
def rmhw(event): #刪除作業
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text="作業刪除成功"))
def addtestsuccess(event): #新增考試成功
    try:
        message = TextSendMessage(  
            text = "考試新增成功"
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
def ttreply(event): #顯示考試
    timeotp=time.strftime("%Y/%m/%d", time.localtime())
    pr=timeotp+" 考試：\n\n--------------------\n\n"
    pr+=googlesheettest.test()
    pr+="\n--------------------\n\nヽ(⊙_⊙)ﾉ📋"
    try:
        message = TextSendMessage(  
            text = pr
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
def rmtt(event): #刪除考試成功
    try:
        message = TextSendMessage(  
            text = "刪除考試成功"
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
def rmbulletboard(event): #刪除公告成功
    try:
        message = TextSendMessage(  
            text = "刪除公告成功"
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
def addbulletboard(event): #新增公告成功
    try:
        message = TextSendMessage(  
            text = "新增公告成功"
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
def bulletboardreply(event): #顯示公告
    pr="公告區：\n\n"
    pr+=googlesheettest.bulletboard()
    try:
        message = TextSendMessage(  
            text = pr
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
def exam(event):#段考
    today = date.today()
    the_past = date(2020,7,9)
    time_to_past= the_past-today
    output="段考還有："+str(time_to_past.days)+"天\n\n"
    output+=googlesheettest.exam()
    try:
        message = TextSendMessage(  
            text = output
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
def notifyon(event): #顯示作業
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text="通知功能已開啟"))
def notifyoff(event): #刪除作業
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text="通知功能已關閉"))