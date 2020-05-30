import mysql.connector
from module import todatabase,authorize
def homework():
    lssh1 = mysql.connector.connect(
    host = todatabase.host(),
    port = "3306",
    user = todatabase.username(),
    password = todatabase.password(),
    database = todatabase.database(),)
    gcpsql= lssh1.cursor()
    sql_select_Query = "select * from homework order by expiretime asc"
    gcpsql.execute(sql_select_Query)
    records = gcpsql.fetchall()
    output=""
    i=0
    for row in records:
        i=i+1
        output+=str(i)+"."+row[2]+" "
        date=row[3]
        output+="("
        for j in range(5,7):
            output+=date[j]
        output+="/"
        for j in range(8,10):
            output+=date[j]
        output+=")\n"
    if (lssh1.is_connected()):
        gcpsql.close()
        lssh1.close()
    return output
def test():
    lssh1 = mysql.connector.connect(
    host = todatabase.host(),
    port = "3306",
    user = todatabase.username(),
    password = todatabase.password(),
    database = todatabase.database(),)
    gcpsql= lssh1.cursor()
    sql_select_Query = "select * from test ORDER BY expiretime ASC"
    gcpsql.execute(sql_select_Query)
    records = gcpsql.fetchall()
    output=""
    i=0
    for row in records:
        i=i+1
        output+=str(i)+"."+row[2]+" "
        date=row[3]
        output+="("
        for j in range(5,7):
            output+=date[j]
        output+="/"
        for j in range(8,10):
            output+=date[j]
        output+=")\n"
    if (lssh1.is_connected()):
        gcpsql.close()
        lssh1.close()
    return output
def bulletboard():
    lssh1 = mysql.connector.connect(
    host = todatabase.host(),
    port = "3306",
    user = todatabase.username(),
    password = todatabase.password(),
    database = todatabase.database(),)
    gcpsql= lssh1.cursor()
    sql_select_Query = "select ID,object from bulletboard order by expiretime asc"
    gcpsql.execute(sql_select_Query)
    records = gcpsql.fetchall()
    output=""
    for row in records:
        output+=str(row[0])+"."+row[1]+"\n\n"
    if (lssh1.is_connected()):
        gcpsql.close()
        lssh1.close()
    return output
def exam():
    lssh1 = mysql.connector.connect(
    host = todatabase.host(),
    port = "3306",
    user = todatabase.username(),
    password = todatabase.password(),
    database = "lssh",)
    gcpsql= lssh1.cursor()
    sql_select_Query = "select * from examG11_social"
    gcpsql.execute(sql_select_Query)
    records = gcpsql.fetchall()
    output=""
    for row in records:
        output+=row[1]+"："+row[2]+"\n"
    if (lssh1.is_connected()):
        gcpsql.close()
        lssh1.close()
    return output
def temperture(i):
    lssh1 = mysql.connector.connect(
    host = todatabase.host(),
    port = "3306",
    user = todatabase.username(),
    password = todatabase.password(),
    database = todatabase.database(),)
    gcpsql= lssh1.cursor()
    output=""
    if(authorize.authtemperture(i)=="yes"):
        sql_select_Query = "select * from body_temperture"
        gcpsql.execute(sql_select_Query)
        records = gcpsql.fetchall()
        output+=" 體溫總表：\n\n"
        for row in records:
            output+=str(row[1])+". "+str(row[3])+" "+str(row[4])+"\n"
        output+="\n輸出結束"
    else:
        output+=" 你的體溫：\n\n"
        morning="""select morning from body_temperture WHERE stu_id=%s"""
        gcpsql.execute(morning,(i,))
        datas=gcpsql.fetchone()
        temp=str(datas)
        output+=temp[1]+temp[2]+temp[3]+temp[4]+" "
        evening="""select evening from body_temperture WHERE stu_id=%s"""
        gcpsql.execute(evening,(i,))
        datas=gcpsql.fetchone()
        temp=str(datas)
        output+=temp[1]+temp[2]+temp[3]+temp[4]
    if(lssh1.is_connected()):
        gcpsql.close()
        lssh1.close()
    return output
