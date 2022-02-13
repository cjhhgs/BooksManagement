import pymysql


def getUserList():
    conn = pymysql.connect(
        host="localhost",
        port=3306,
        db="bookmanage",
        user="root",
        passwd="123456",
        charset='utf8'
    )
    cur = conn.cursor()
    sql = "select * from user"
    cur.execute(sql)
    content = cur.fetchall()
    cur.close()
    conn.close()
    return content

def getTable(tablename):
    conn = pymysql.connect(
        host="localhost",
        port=3306,
        db="bookmanage",
        user="root",
        passwd="123456",
        charset='utf8'
    )
    cur = conn.cursor()
    sql = "select * from %s"%\
        (tablename)
    cur.execute(sql)
    content = cur.fetchall()

    sql = "show fields from %s"%\
        (tablename)
    cur.execute(sql)
    labels = cur.fetchall()
    labels = [l[0] for l in labels]
    cur.close()
    conn.close()

    res = {"content":content,"lables":labels}
    return res

def getRecord(username):
    if username == None:
        return None
    conn = pymysql.connect(
        host="localhost",
        port=3306,
        db="bookmanage",
        user="root",
        passwd="123456",
        charset='utf8'
    )
    cur = conn.cursor()
    sql = "select * from record"
    cur.execute(sql)
    content = cur.fetchall()
    cur.close()
    conn.close()

    res = []
    for i in content:
        if(i[1]==username):
            res.append(i)
    return {"record":res}


# 重要的处理函数，处理各种post请求
# req = {way:"xxx",info:"xxx"}, user = "name"
# returnStatus:
# 0 : 成功
# 1 : 没有登录用户
# 2 : 书的数量为0，无法借书
# 3 : 数据库错误
def handle_requset(req,user = None):
    way = req['way']
    info = req['info']
    print(way)
    print(info)
    returnStatus = 0

    if way == "borrow":
        returnStatus = handle_borrow(info,user)
    if way == "returnBook":
        returnStatus = handle_returnBook(info,user)
    if way == "addItem":
        returnStatus = handle_addItem(info,user)
    if way == "deleteItem":
        returnStatus = handle_deleteItem(info,user)
    if way == "modifyItem":
        returnStatus = handle_modifyItem(info,user)
    return returnStatus

#借书的处理函数
def handle_borrow(info,user):

    returnStatus = 0
    if user == None:
        returnStatus = 1    #无用户，返回错误
        return returnStatus

    bookid = int(info)
    num = numOfBook(bookid)
    if num == 0:
        returnStatus = 2    #书的数量为0
        return returnStatus
    
    if(ifBorrow(bookid,user)==True):
        returnStatus = 4    #已经借过书
        return returnStatus


    conn = pymysql.connect(
        host="localhost",
        port=3306,
        db="bookmanage",
        user="root",
        passwd="123456",
        charset='utf8'
    )
    cur = conn.cursor()
    sql = """
        update book_list set number = %d where book_id = %d;
        
    """%\
        (num-1,bookid)
    sql2 = """insert into record ( username, book_id )
                       VALUES
                       ("%s",%d);"""%\
                           (user,bookid)
    try:
        cur.execute(sql)
        conn.commit()
        cur.execute(sql2)
        conn.commit()
        returnStatus = 0
    except:
        print('update error')
        returnStatus = 3
    
    cur.close()
    conn.close()

    return returnStatus

#还书的处理函数
def handle_returnBook(info,user):
    record_id = info["record_id"]
    username = info["username"]
    book_id = info["book_id"]
    num = numOfBook(book_id)

    returnStatus = 0
    if user == None:
        returnStatus = 1    #无用户，返回错误
        return returnStatus
    
    if user != username:
        returnStatus = 3
        return returnStatus
    
    conn = pymysql.connect(
        host="localhost",
        port=3306,
        db="bookmanage",
        user="root",
        passwd="123456",
        charset='utf8'
    )
    cur = conn.cursor()
    sql = "delete from record where id = %d"%\
        (record_id)
    sql2 = """update book_list set number = %d where book_id = %d;"""%\
        (num+1,book_id)
    try:
        cur.execute(sql)
        conn.commit()
        cur.execute(sql2)
        conn.commit()
        returnStatus = 0
    except:
        print('update error')
        returnStatus = 3
    cur.close()
    conn.close()
    return returnStatus


#添加表项的处理函数
# info = {
#    table:"xx",
#    item:["xx","xx",……]
# }
def handle_addItem(info,user):
    returnStatus=0
    table = info["table"]
    item = info["item"]
    print(item)
    if table == "book_list":
        sql = """INSERT INTO book_list ( name, auther,price,date,number )
                       VALUES
                       ("%s","%s",%s,"%s",%s );"""%\
                           (item[1],item[2],item[3],item[4],item[5])
    elif table == "user":
        sql = """INSERT INTO user ( name, password,if_manager )
                       VALUES
                       ("%s","%s","%s");"""%\
                           (item[1],item[2],item[3])
    conn = pymysql.connect(
        host="localhost",
        port=3306,
        db="bookmanage",
        user="root",
        passwd="123456",
        charset='utf8'
    )
    cur = conn.cursor()
    try:
        cur.execute(sql)
        conn.commit()
        print("success")
    except:
        print("error")
        returnStatus=3
    
    cur.close()
    conn.close()
    return returnStatus

#删除表项
# info = {
#   table:'xxx'
#   id:xxx
# }
def handle_deleteItem(info,user):
    returnStatus=0
    table = info["table"]
    id = info["id"]
    if table == 'book_list':
        sql = "delete from book_list where book_id=%s"%\
            (id)
    elif table == 'user':
        sql = "delete from user where id = %s"%\
            (id)
    conn = pymysql.connect(
        host="localhost",
        port=3306,
        db="bookmanage",
        user="root",
        passwd="123456",
        charset='utf8'
    )
    cur = conn.cursor()
    try:
        cur.execute(sql)
        conn.commit()
        print("success")
    except:
        print("error")
        returnStatus=3
    
    cur.close()
    conn.close()
    return returnStatus

# info={
#   table:'xxx'
#   oldInfo:[],
#   newInfo:[]
# }
def handle_modifyItem(info,user):
    returnStatus = 0
    table = info['table']
    oldInfo = info['oldInfo']
    newInfo = info['newInfo']
    id = oldInfo[0]

    if table=='book_list':
        sql = "update book_list set name='%s', auther='%s', price=%s, date='%s', number=%s where book_id = %s"%\
            (newInfo[1],newInfo[2],newInfo[3],newInfo[4],newInfo[5],id)
    elif table=='user':
        sql = "update user set name='%s', password='%s', if_manager='%s' where id =%s"%\
            (newInfo[1],newInfo[2],newInfo[3],id)
    conn = pymysql.connect(
        host="localhost",
        port=3306,
        db="bookmanage",
        user="root",
        passwd="123456",
        charset='utf8'
    )
    cur = conn.cursor()
    try:
        cur.execute(sql)
        conn.commit()
        print("success")
    except:
        print("error")
        returnStatus=3
    
    cur.close()
    conn.close()
    return returnStatus


def numOfBook(bookid):
    conn = pymysql.connect(
        host="localhost",
        port=3306,
        db="bookmanage",
        user="root",
        passwd="123456",
        charset='utf8'
    )
    cur = conn.cursor()
    sql = "select number from book_list where book_id = %d"%\
        (bookid)
    cur.execute(sql)
    content = cur.fetchall()
    cur.close()
    conn.close()
    num = content[0][0]
    return num

def ifBorrow(bookid,username):
    conn = pymysql.connect(
        host="localhost",
        port=3306,
        db="bookmanage",
        user="root",
        passwd="123456",
        charset='utf8'
    )
    cur = conn.cursor()
    sql = "select * from record"
    cur.execute(sql)
    content = cur.fetchall()
    cur.close()
    conn.close()

    for i in content:
        if(i[1]==username and i[2]==bookid):
            return True
    return False


if __name__ =="__main__":
    
    req = {
        'way': 'addItem', 
        'info': {
            'table':"book_list",
            'item':[1,'时间简史','xxx',31,'2019-6-6',3]
        }
    }
    handle_requset(req,'root')
    
    