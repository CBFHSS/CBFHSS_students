from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from module import func,todatabase,authorize

import math
import sys
import datetime
from datetime import date,timedelta
import time
import calendar
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import mysql.connector

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):
                if isinstance(event.message, TextMessage):
                    mtext = event.message.text
                    if mtext == "使用方法":
                        func.manual(event)
                    #新增作業
                    if mtext[0] == 'a' and mtext[1]=='d' and mtext [2]=='d' and mtext [3]=='h' and mtext[4]=='w':
                        auth=event.source.user_id
                        if(authorize.authaddrm(auth)=="yes"):
                            lssh1 = mysql.connector.connect(
                            host = todatabase.host(),
                            port = "3306",
                            user = todatabase.username(),
                            password = todatabase.password(),
                            database = todatabase.database(),)
                            gcpsql= lssh1.cursor()
                            timestamp=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                            row=""
                            flag=0
                            exp=0
                            avoid=len(mtext)
                            for i in range (6,avoid):
                                if(mtext[i]=="s" and mtext[i+1]=="e" and mtext[i+2]=="t"):
                                    flag=1 #標記要設定截止日期
                                    count=0 #欲講字串與數字轉換的變數
                                    expt=[] #輸入的截止日期 (X天後)
                                    for j in range (i+4,avoid): #將字串加入list中
                                        x=0
                                        expt.insert(x,mtext[j])
                                        x+=1
                                    for j in range (0,len(expt)): #從list取出，轉會韋數字格式
                                        if(expt[j])!=0:
                                            exp+=int(expt[j])*(pow(10,count)) 
                                            count+=1
                                        else:
                                            exp+=pow(10,count)
                                            count+=1
                                    row=""
                                    setpoint=i
                                    for j in range (6,setpoint): row+=mtext[j]
                                    break
                            if(flag==0):
                                exp=10 
                                for j in range (6,avoid): 
                                    row+=mtext[j]
                            now=date.today()
                            dta=timedelta(days=exp)
                            ans=now+dta
                            datefinal = ans.strftime("%Y/%m/%d")
                            target="""INSERT into homework (createtime,object,expiretime) values (%s,%s,%s)"""
                            record=(timestamp,row,datefinal)
                            gcpsql.execute(target,(record))
                            lssh1.commit()
                            if (lssh1.is_connected()):
                                gcpsql.close()
                                lssh1.close()
                            func.addhwsuccess(event)
                            return mtext
                        else: func.unauthorize(event)
                    #顯示作業
                    if mtext == '作業':
                        func.hwreply(event)
                    #刪除作業
                    if mtext[0] == 'r' and mtext[1]=='m' and mtext [2]=='h' and mtext [3]=='w':
                        auth=event.source.user_id
                        if(authorize.authaddrm(auth)=="yes"):
                            lssh1 = mysql.connector.connect(
                            host = todatabase.host(),
                            port = "3306",
                            user = todatabase.username(),
                            password = todatabase.password(),
                            database =todatabase.database(),)
                            gcpsql= lssh1.cursor()
                            compare=""
                            avoid=len(mtext)#算有幾格
                            for i in range (5,len(mtext)):
                                compare+=mtext[i]#從第5格算數字
                            target=int(compare)
                            sql_select_Query = "select * from homework order by expiretime asc"
                            gcpsql.execute(sql_select_Query)
                            records = gcpsql.fetchall()
                            delete=records[target-1][0]
                            sql_Delete_query = """DELETE FROM homework WHERE ID= %s"""
                            gcpsql.execute(sql_Delete_query, (delete,))
                            lssh1.commit()
                            if(lssh1.is_connected()):
                                gcpsql.close()
                                lssh1.close()
                            func.rmhw(event)
                            return mtext
                        else: func.unauthorize(event)
                    #新增考試
                    if mtext[0] == 'a' and mtext[1]=='d' and mtext [2]=='d' and mtext[3]=='t' and mtext[4]=='t':
                        auth=event.source.user_id
                        if(authorize.authaddrm(auth)=="yes"):                  
                            lssh1 = mysql.connector.connect(
                            host = todatabase.host(),
                            port = "3306",
                            user = todatabase.username(),
                            password = todatabase.password(),
                            database = todatabase.database(),)
                            gcpsql= lssh1.cursor()                    
                            timestamp=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                            row=""
                            flag=0
                            exp=0
                            avoid=len(mtext)
                            for i in range (6,avoid):
                                if(mtext[i]=="s" and mtext[i+1]=="e" and mtext[i+2]=="t"):
                                    flag=1
                                    count=0
                                    expt=[]
                                    for j in range (i+4,avoid): 
                                        x=0
                                        expt.insert(x,mtext[j])
                                        x+=1
                                    for j in range (0,len(expt)):
                                        if(expt[j])!=0:
                                            exp+=int(expt[j])*(pow(10,count)) 
                                            count+=1
                                        else:
                                            exp+=pow(10,count)
                                            count+=1
                                    #exp=int(mtext[i+4])
                                    setpoint=i
                                    row=""
                                    for j in range (6,setpoint): row+=mtext[j]
                                    break
                            if(flag==0):
                                exp=10  
                                for j in range (6,avoid): 
                                    row+=mtext[j]
                            now=date.today()
                            dta=timedelta(days=exp)
                            ans=now+dta
                            datefinal = ans.strftime("%Y/%m/%d")
                            target="""INSERT into test (createtime,object,expiretime) values (%s,%s,%s)"""
                            record=(timestamp,row,datefinal)
                            gcpsql.execute(target,(record))
                            lssh1.commit()
                            if (lssh1.is_connected()):
                                gcpsql.close()
                                lssh1.close()
                            func.addtestsuccess(event)
                            return mtext
                        else: func.unauthorize(event)
                    #顯示考試
                    if mtext == '考試':
                        func.ttreply(event)
                    #刪除考試
                    if mtext[0] == 'r' and mtext[1]=='m' and mtext [2]=='t' and mtext [3]=='t':
                        auth=event.source.user_id
                        if(authorize.authaddrm(auth)=="yes"):
                            lssh1 = mysql.connector.connect(
                            host = todatabase.host(),
                            port = "3306",
                            user = todatabase.username(),
                            password = todatabase.password(),
                            database = todatabase.database(),)
                            gcpsql= lssh1.cursor()
                            compare=""
                            avoid=len(mtext)#算有幾格
                            for i in range (5,len(mtext)):
                                compare+=mtext[i]#從第5格算數字
                            target=int(compare)
                            sql_select_Query = "select * from test order by expiretime asc"
                            gcpsql.execute(sql_select_Query)
                            records = gcpsql.fetchall()
                            delete=records[target-1][0]
                            sql_Delete_query = """DELETE FROM test WHERE ID= %s"""
                            gcpsql.execute(sql_Delete_query, (delete,))
                            lssh1.commit()
                            if(lssh1.is_connected()):
                                gcpsql.close()
                                lssh1.close()
                            func.rmtt(event)
                        else:
                            func.unauthorize(event)
                        return mtext
                    if mtext[0] == "#": #新增公告
                        auth=event.source.user_id
                        if(authorize.authaddrm(auth)=="yes"):                  
                            lssh1 = mysql.connector.connect(
                            host = todatabase.host(),
                            port = "3306",
                            user = todatabase.username(),
                            password = todatabase.password(),
                            database = todatabase.database(),)
                            gcpsql= lssh1.cursor()                    
                            timestamp=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                            row=""
                            flag=0
                            exp=0
                            avoid=len(mtext)
                            for i in range (2,avoid):
                                if(mtext[i]=="s" and mtext[i+1]=="e" and mtext[i+2]=="t"):
                                    flag=1
                                    count=0
                                    expt=[]
                                    for j in range (i+4,avoid): 
                                        x=0
                                        expt.insert(x,mtext[j])
                                        x+=1
                                    for j in range (0,len(expt)):
                                        if(expt[j])!=0:
                                            exp+=int(expt[j])*(pow(10,count)) 
                                            count+=1
                                        else:
                                            exp+=pow(10,count)
                                            count+=1
                                    #exp=int(mtext[i+4])
                                    setpoint=i
                                    row=""
                                    for j in range (2,setpoint): row+=mtext[j]
                                    break
                            if(flag==0):
                                exp=10  
                                for j in range (2,avoid): 
                                    row+=mtext[j]
                            now=date.today()
                            dta=timedelta(days=exp)
                            ans=now+dta
                            datefinal = ans.strftime("%Y/%m/%d")
                            target="""INSERT into bulletboard (createtime,object,expiretime) values (%s,%s,%s)"""
                            record=(timestamp,row,datefinal)
                            gcpsql.execute(target,(record))
                            lssh1.commit()
                            if (lssh1.is_connected()):
                                gcpsql.close()
                                lssh1.close()
                            func.addbulletboard(event)
                            return mtext
                        else: func.unauthorize(event)
                    #顯示公告
                    if mtext == '公告':
                        func.bulletboardreply(event)
                    #刪除公告
                    if mtext[0] == 'r' and mtext[1]=='m' and mtext [2]=='b' and mtext [3]=='b':
                        auth=event.source.user_id
                        if(authorize.authaddrm(auth)=="yes"):
                            lssh1 = mysql.connector.connect(
                            host = todatabase.host(),
                            port = "3306",
                            user = todatabase.username(),
                            password = todatabase.password(),
                            database = todatabase.database(),)
                            gcpsql= lssh1.cursor()
                            compare=""
                            avoid=len(mtext)#算有幾格
                            for i in range (5,len(mtext)):
                                compare+=mtext[i]#從第5格算數字
                            target=int(compare)
                            sql_select_Query = "select * from bulletboard order by expiretime asc"
                            gcpsql.execute(sql_select_Query)
                            records = gcpsql.fetchall()
                            delete=records[target-1][0]
                            sql_Delete_query = """DELETE FROM bulletboard WHERE ID= %s"""
                            gcpsql.execute(sql_Delete_query, (delete,))
                            lssh1.commit()
                            if(lssh1.is_connected()):
                                gcpsql.close()
                                lssh1.close()
                            func.rmbulletboard(event)
                        else:
                            func.unauthorize(event)
                        return mtext
                    if mtext=="推播通知":
                        lssh1 = mysql.connector.connect(
                        host = "127.0.0.1",
                        port = "3306",
                        user = todatabase.username(),
                        password = todatabase.password(),
                        database = todatabase.database(),)
                        gcpsql= lssh1.cursor()
                        id=event.source.user_id
                        sql_select_Query = "select line_id,notify from user_id"
                        gcpsql.execute(sql_select_Query)
                        records = gcpsql.fetchall()
                        notify=0
                        i=1
                        for row in records:
                            if(row[0]==id):
                                notify=row[1]
                                break 
                            i+=1
                        if (notify==0): notify=1
                        elif (notify==1): notify=0
                        update="""UPDATE user_id SET notify=%s WHERE stu_id=%s"""
                        value=(notify,i)
                        gcpsql.execute(update,(value))
                        lssh1.commit()
                        if (notify==0): func.notifyoff(event)
                        elif (notify==1): func.notifyon(event)
                    #段考
                    if mtext == "段考" :
                        func.exam(event)
                    if mtext== "體溫查詢":
                        func.seetemperture(event)
                    #體溫
                    elif mtext[0]=="體" and mtext[1]=="溫":
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
                        insertroll=0
                        for row in records:
                            if row[3] == str(userid):
                                insertroll=int(row[1])
                        result=time.localtime()
                        temp=mtext[3]+mtext[4]+mtext[5]+mtext[6]
                        if(result.tm_hour<=12):
                            target="""UPDATE body_temperture set morning=%s WHERE ID=%s"""
                            record=(temp,insertroll)
                            gcpsql.execute(target,(record))
                            lssh1.commit()
                        if(result.tm_hour>12):
                            target="""UPDATE body_temperture set evening=%s WHERE ID=%s"""
                            record=(temp,insertroll)
                            gcpsql.execute(target,(record))
                            lssh1.commit()
                        if (lssh1.is_connected()):
                            gcpsql.close()
                            lssh1.close()
                        func.addtemperturesuccess(event)
                    if mtext[0]=="s" and mtext[1]=="e" and mtext[2]=="t":#設定座號
                        lssh1 = mysql.connector.connect(
                        host = todatabase.host(),
                        port = "3306",
                        user = todatabase.username(),
                        password = todatabase.password(),
                        database = todatabase.database(),)
                        gcpsql= lssh1.cursor()
                        user_id=event.source.user_id
                        profile=line_bot_api.get_profile(user_id)
                        name=profile.display_name
                        expt=""
                        for j in range (4,len(mtext)):
                            expt+=mtext[j]
                        check=int(expt)
                        target="""select rw FROM user_id"""
                        gcpsql.execute(target)
                        records = gcpsql.fetchall()
                        if(records[check-1][0]==1):
                            target="""UPDATE user_id SET line_id=%s, nickname=%s WHERE stu_id=%s"""
                            record=(user_id,name,expt)
                            gcpsql.execute(target,(record))
                            lssh1.commit()
                            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="新增座號成功"))
                        else: line_bot_api.reply_message(event.reply_token,TextSendMessage(text="本座號已設定並由管理員確認，若需更改請填寫錯誤回報表單"))
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="新增座號成功"))
                        if (lssh1.is_connected()):
                            gcpsql.close()
                            lssh1.close()
                    # user_id
                    if mtext!= "":
                        auth_json_path='linebotlssh-a0cc46d0d13a.json'
                        gss_scopes=['https://www.googleapis.com/auth/spreadsheets']
                        credentials= ServiceAccountCredentials.from_json_keyfile_name(auth_json_path,gss_scopes)
                        gss_client =gspread.authorize(credentials)
                        spreadsheets_key='1FJaCeiPDrkkPwFMeOSDfohdOM76v-JmWV1NzljfRBNE'
                        sheet=gss_client.open_by_key(spreadsheets_key).sheet1
                        user_id = event.source.user_id
                        profile=line_bot_api.get_profile(user_id)
                        a=str(user_id)
                        flag=0
                        for i in range (2,30):
                            if (sheet.cell(i,3).value) == a:
                                if (sheet.cell(i,2).value) == "":
                                    sheet.update_cell(i,2,profile.display_name)
                                    flag=1
                                else:
                                    flag=1    
                        if(flag==0):
                            timestamp=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                            a=len(mtext)
                            output=""
                            for i in range(1,a): output+=mtext[i] 
                            output=[timestamp,profile.display_name,user_id]
                            sheet.insert_row(output,2)
        return HttpResponse()
    else:
        return HttpResponseBadRequest()