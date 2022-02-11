import pymysql

def ifManager(user):
    
    conn = pymysql.connect(
        host="localhost",
        port=3306,
        db="bookmanage",
        user="root",
        passwd="123456",
        charset='utf8'
    )
    cur = conn.cursor()
    sql = "select if_manager from user where name = '%s';"%\
        (user)
    cur.execute(sql)
    content = cur.fetchall()
    cur.close()
    conn.close()
    if content == None:
        return False
    res = content[0][0]
    if res == "Y":
        return True
    return False

if __name__ == '__main__':
    print(ifManager('cjh'))