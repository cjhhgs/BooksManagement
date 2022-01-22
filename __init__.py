
import flask
import pymysql

conn = pymysql.connect(
    host="localhost",
    port=3306,
    db="bookmanage",
    user="root",
    passwd="123456",
    charset='utf8'
)

def creat_app():
    app = flask.Flask(__name__,instance_relative_config=True)
    app.secret_key = 'div'
    @app.route('/bookmanage')
    def index_page():
        return flask.render_template('index.html')
    @app.route('/bookmanage/login',methods=['POST','GET'])
    def login():
        if flask.request.method == 'GET':
            return flask.render_template('login.html')
        if flask.request.method == 'POST':
            user_name = flask.request.form.get('username')
            password = flask.request.form.get('password')
            print(user_name)
            print(password)
            #return flask.render_template('main.html',user = user_name)
            return flask.redirect('/bookmanage/main')
    
    @app.route('/bookmanage/main',)
    def main_page():
        cur = conn.cursor()
        sql = "select * from book_list"
        cur.execute(sql)
        content = cur.fetchall()

        sql = "show fields from book_list"
        cur.execute(sql)
        labels = cur.fetchall()
        labels = [l[0] for l in labels]

        return  flask.render_template('main.html',labels=labels,content=content)
    return app

if __name__ == '__main__':
    app = creat_app()
    app.run(
        host = '127.0.0.1',
        port=80,
        debug=True
    )