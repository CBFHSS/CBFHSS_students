from datetime import datetime
import os
from apscheduler.schedulers.blocking import BlockingScheduler
from linebot import LineBotApi
from linebot.models import TextSendMessage, ImageSendMessage, StickerSendMessage, LocationSendMessage, QuickReply, QuickReplyButton, MessageAction
from module import todatabase
import datetime
from datetime import date
import time
import calendar
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
import sys
import mysql.connector

users=[]
pr=""
hmw=""
output=""
def userpick():
    users.clear()
    lssh1 = mysql.connector.connect(
    host = todatabase.host(),
    port = "3306",
    user = todatabase.username(),
    password = todatabase.password(),
    database = todatabase.database(),)
    gcpsql= lssh1.cursor()
    gcpsql= lssh1.cursor()
    sql_select_Query = "select line_id,notify from user_id WHERE line_id IS NOT NULL"
    gcpsql.execute(sql_select_Query)
    records = gcpsql.fetchall()
    for row in records:
        if(row[1]==1):
            users.append(row[0])
def homework():
    lssh1 = mysql.connector.connect(
    host = todatabase.host(),
    port = "3306",
    user = todatabase.username(),
    password = todatabase.password(),
    database = todatabase.database(),)
    gcpsql= lssh1.cursor()
    timeotp=time.strftime("%Y/%m/%d", time.localtime())
    pr=timeotp+"放學推播：\n--------------------\n作業：\n\n"
    sql_select_Query = "select * from homework ORDER BY expiretime ASC"
    gcpsql.execute(sql_select_Query)
    records = gcpsql.fetchall()
    i=0
    for row in records:
        i=i+1
        pr+=str(i)+"."+row[2]
        date=row[3]
        datecor=date[5]+date[6]+"/"+date[8]+date[9]
        pr+=" ("+datecor+")\n"
    pr+="\n"
    if(lssh1.is_connected()):
        gcpsql.close()
        lssh1.close()
    return pr
def test():
    lssh1 = mysql.connector.connect(
    host = todatabase.host(),
    port = "3306",
    user = todatabase.username(),
    password = todatabase.password(),
    database = todatabase.database(),)
    gcpsql= lssh1.cursor()
    pr="--------------------\n考試：\n\n"
    sql_select_Query = "select * from test ORDER BY expiretime ASC"
    gcpsql.execute(sql_select_Query)
    records = gcpsql.fetchall()
    i=0
    for row in records:
        i=i+1
        pr+=str(i)+"."+row[2]
        date=row[3]
        datecor=date[5]+date[6]+"/"+date[8]+date[9]
        pr+=" ("+datecor+")\n"
    pr+="\n"
    if(lssh1.is_connected()):
        gcpsql.close()
        lssh1.close()
    return pr
def teacher():
    lssh1 = mysql.connector.connect(
    host = todatabase.host(),
    port = "3306",
    user = todatabase.username(),
    password = todatabase.password(),
    database= todatabase.database())
    gcpsql= lssh1.cursor()
    sqlselect = """select ID,object from bulletboard ORDER BY expiretime ASC"""
    gcpsql.execute(sqlselect)
    records = gcpsql.fetchall()
    output=""
    i=0
    for row in records:
        i=i+1
        output+=str(i)+"."+row[1]+"\n\n"
    if(lssh1.is_connected()):
        gcpsql.close()
        lssh1.close()
    return output
def push():
    channel_access_token='Your LINE Channel Access Token'
    line_bot_api = LineBotApi(channel_access_token)    
    output=""
    userpick()
    output+=homework()
    output+=test()
    output+="\n--------------------\n"
    output+=teacher()
    a=len(users)
    #print(a)
    for i in range (0,a):
        user=users[i]
        line_bot_api.push_message(user, TextSendMessage(text=output))