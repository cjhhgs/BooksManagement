## 项目使用说明

运行环境：win10, python3.8，mysql8.0.23

#### 一、准备

在使用前，请使用pip安装依赖：

```
pip install pymysql

pip install flask

pip install flask_login
```

若有后续执行中有错误提示，请根据提示安装对应依赖



请安装mysql 8.0版本，教程请参照：[（二）史上最详细MySQL8版本以上安装教程 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/433040834)

其中，用户名设为root，密码设为123456



#### 二、初始化数据库

在vscode中打开文件夹bookmanage

打开新终端，执行`python init.py` ,如下：

```
PS H:\gitdemo\bookmanage> python init.py
请复制以下命令并在mysql中输入
source H:/gitdemo/bookmanage/sql_file/dbinit.sql
source H:/gitdemo/bookmanage/sql_file/data_insert.sql    
source H:/gitdemo/bookmanage/sql_file/userinfo_insert.sql
Enter password: 

```

输入密码123456后，如下：

```
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 51
Server version: 8.0.23 MySQL Community Server - GPL

Copyright (c) 2000, 2021, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql>
```

依次复制并粘贴给出的3条语句：

```
source H:/gitdemo/bookmanage/sql_file/dbinit.sql
source H:/gitdemo/bookmanage/sql_file/data_insert.sql    
source H:/gitdemo/bookmanage/sql_file/userinfo_insert.sql
```

之后`ctrl+Z` 退出mysql



#### 三、部署网站

`cd flaskr` 进入flaskr目录

`python __init__.py` ，启动网站

```
PS H:\gitdemo\bookmanage> cd flaskr
PS H:\gitdemo\bookmanage\flaskr> python __init__.py
 * Serving Flask app '__init__' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 649-158-124
 * Running on all addresses.
   WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://192.168.31.172:8088/ (Press CTRL+C to quit)


```

之后，在浏览器中访问`http://192.168.31.172:8088/bookmanage` 即可进入主页

注意，若有提示错误，有可能是8088端口被占用，请修改运行端口



#### 四、登录

内置用户有

管理员 root, 123456

普通用户 cjh, 123456

若要添加管理图书或用户，请登录管理员账户