import flask_login
import database

def get_userinfo_by_name(name):
    #print(database.getUserList())
    for user in database.getUserList():
        if user[1] == str(name):
            return{
                "id":user[0],
                "name":user[1],
                "password":user[2],
            }
    return None

class User(flask_login.UserMixin):
    def __init__(self,user):
        # user = {"id":id "name":name "password":password }
        self.id = user.get("id")
        self.username = user.get("name")
        self.password = user.get("password")
    
    def verify_password(self, password):
        # 密码验证
        if self.password is None:
            return False
        return self.password == password
    
    def get_id(self):
        return self.id

    @staticmethod
    def get(user_id):
        # 根据id 获取用户实体
        if not user_id:
            return None
        
        for user in database.getUserList() :
            if user[0] == int(user_id):
                user =  {
                    "id": user[0],
                    "name": user[1],
                    "password": user[2],
                }
                return User(user)
        return None
