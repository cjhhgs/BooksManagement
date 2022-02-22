import os

path = os.getcwd()
sql = "source "+path+r"\sql_file\dbinit.sql"
sql2 = "source "+path+r"\sql_file\data_insert.sql"
sql3 = "source "+path+r"\sql_file\userinfo_insert.sql"

sql=sql.replace('\\','/')
sql2=sql2.replace('\\','/')
sql3=sql3.replace('\\','/')
print("请复制以下命令并在mysql中输入")
print(sql)
print(sql2)
print(sql3)
os.system("mysql -u root -p")

print("初始化完成")
