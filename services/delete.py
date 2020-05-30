import os
from apscheduler.schedulers.blocking import BlockingScheduler

import datetime
from datetime import date, datetime, timedelta
import time
import calendar
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import sys
import mysql.connector
from module import todatabase

def homework():
    lssh1 = mysql.connector.connect(
    host = todatabase.host(),
    port = "3306",
    user = todatabase.username(),
    password = todatabase.password(),
    database=todatabase.database(),)
    gcpsql= lssh1.cursor()
    sql_select_Query = "select * from homework"
    gcpsql.execute(sql_select_Query)
    records = gcpsql.fetchall()
    for row in records:
        dateString = row[3]
        dateFormatter = "%Y/%m/%d"
        a=datetime.strptime(dateString, dateFormatter)
        #a=a+timedelta(days=1)
        if(datetime.now()>a):
            sql_Delete_query = """DELETE FROM homework WHERE ID= %s"""
            homework=int(row[0])
            gcpsql.execute(sql_Delete_query, (homework,))
            lssh1.commit()
            if(lssh1.is_connected()):
                gcpsql.close()
                lssh1.close()

def test():
    lssh1 = mysql.connector.connect(
    host = todatabase.host(),
    port = "3306",
    user = todatabase.username(),
    password = todatabase.password(),
    database=todatabase.database(),)
    gcpsql= lssh1.cursor()
    sql_select_Query = "select * from test"
    gcpsql.execute(sql_select_Query)
    records = gcpsql.fetchall()
    for row in records:
        dateString = row[3]
        #if(dateString==""): break
        dateFormatter = "%Y/%m/%d"
        a=datetime.strptime(dateString, dateFormatter)
        #a=a+timedelta(days=1)
        if(datetime.now()>a):
            sql_Delete_query = """DELETE FROM test WHERE ID= %s"""
            test=row[0]
            gcpsql.execute(sql_Delete_query, (test,))
            lssh1.commit()
            if(lssh1.is_connected()):
                gcpsql.close()
                lssh1.close()
def run():
    homework()
    test()