import mysql.connector
from module import todatabase
def authtemperture(i):
    if(i>=1 and i<=25): return "yes"
    else: return "no"
def authaddrm(auth):
    lssh1 = mysql.connector.connect(
    host = todatabase.host(),
    port = "3306",
    user = todatabase.username(),
    password = todatabase.password(),
    database = todatabase.database(),)
    gcpsql= lssh1.cursor()
    user_id="""select * from user_id"""
    gcpsql.execute(user_id)
    records = gcpsql.fetchall()
    i=0
    for row in records:
        if row[3] == auth: 
            i=row[1]
            break
    if(i>=1 and i<=25): auth="yes"
    else: auth="no"
    if(lssh1.is_connected()):
        gcpsql.close() 
        lssh1.close()
    return auth