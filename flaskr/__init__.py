

from ast import arg
import flask
import flask_login
import pymysql
import os
import user
from user import get_userinfo_by_name,User
from flask_login import LoginManager
import json
import database
import manage


def creat_app(test_config=None):
    # create and configure the app
    app = flask.Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    #用户登录管理
    login_manger = LoginManager()
    login_manger.init_app(app)
    login_manger.login_view = 'login'

    @login_manger.user_loader
    def load_user(user_id):
        return user.User.get(user_id)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    

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
            
            userinfo = get_userinfo_by_name(user_name)
            emsg = None
            if userinfo is None:
                emsg = 'user not exists'
            else:
                user = User(userinfo)
                if user.verify_password(password):
                    flask_login.login_user(user)
                else:
                    emsg = "password error"
            
            if emsg is None:
                return flask.redirect('/bookmanage/main')
            
            else:
                flask.flash(emsg)
                return flask.redirect('/bookmanage/login')
                
            #return flask.render_template('main.html',user = user_name)
            
    
    @app.route('/bookmanage/main')
    @flask_login.login_required
    def main_page():
        userame = None
        if hasattr(flask_login.current_user, 'username'):
            userame = flask_login.current_user.username
        print('current user: ', userame)

        

        return  flask.render_template('main.html')

    @app.route('/bookmanage/user')
    @flask_login.login_required
    def user_page():
        userame = None
        if hasattr(flask_login.current_user, 'username'):
            userame = flask_login.current_user.username
        print('current user: ', userame)
        return  flask.render_template('user.html')

    @app.route('/bookmanage/database',methods=['POST','GET'])
    def book():
        if flask.request.method == 'GET':
            args = flask.request.args.to_dict()
            if args == {}:
                args = 'book_list'
            else:
                print(args)
                args = args['table']
            res = database.getTable(args)
            return res

        if flask.request.method == 'POST':
            print('post')
            res = json.loads(flask.request.data)
            print('get data:')
            print(res)
            user = getattr(flask_login.current_user, 'username', None)
            print('user:'+user)
            returnStatus = database.handle_requset(res,user)
            return {'statu': returnStatus, 'info': "ok"}
        
    @app.route('/bookmanage/record')
    @flask_login.login_required
    def record():
        user = getattr(flask_login.current_user, 'username', None)
        res = database.getRecord(user)
        return res

    @app.route('/bookmanage/manage')
    @flask_login.login_required
    def manage_page():
        user = getattr(flask_login.current_user, 'username', None)
        res = manage.ifManager(user)
        if res == False:
            flask.flash('无权限')
            return flask.redirect('/bookmanage/main')
        else:
            return flask.render_template('manage.html')
        

    return app

if __name__ == '__main__':
    app = creat_app()
    app.run(
        host = '0.0.0.0',
        port=8088,
        debug=True
    )