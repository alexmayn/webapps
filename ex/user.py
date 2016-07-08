from werkzeug.security import check_password_hash
from ex import db

# User class - using for login/logout
class User(db.Document):
    username = db.StringField(max_length=255, required=True)
    password = db.StringField(max_length=255, required=True)
    isadmin = db.StringField(max_length=255, required=True)


    #def __init__(self, username):
    #    self.username = username
    #    self.isadmin = False
    #    self.email = None

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

    @staticmethod
    def validate_login(password_hash, password):
        return check_password_hash(password_hash, password) # embeded func for calculate hash
