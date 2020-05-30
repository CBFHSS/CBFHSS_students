from datetime import date,timedelta
import mysql.connector
from module import todatabase
def run():
    lssh1 = mysql.connector.connect(
    host = todatabase.host(),
    port = "3306",
    user = todatabase.username(),
    password = todatabase.password(),
    database=todatabase.database(),)
    gcpsql= lssh1.cursor()
    today=date.today()
    dta=timedelta(days=1)
    now=today-dta
    ans=now.strftime("%m%d")
    name="morning_"+ans
    new_column = """ALTER TABLE body_temperture Change morning `%s` FLOAT""" 
    gcpsql.execute(new_column,(name, ))
    lssh1.commit()
    name="evening_"+ans
    new_column = """ALTER TABLE body_temperture Change evening `%s` FLOAT"""
    gcpsql.execute(new_column,(name, ))
    lssh1.commit()
    new_column = "ALTER TABLE body_temperture ADD morning FLOAT after nickname"
    gcpsql.execute(new_column)
    lssh1.commit()
    new_column = "ALTER TABLE body_temperture ADD evening FLOAT after morning"
    gcpsql.execute(new_column)
    lssh1.commit()
    if(lssh1.is_connected()):
        gcpsql.close()
        lssh1.close()

        
    