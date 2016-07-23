from flask import g
from ex import app

# Check user for admin rights
def check_admin():
        try:
          user_obj = g.user  # get global var
        except:
          return False       # exit if user is not define
        # Find user in DB
        user = app.config['USERS_COLLECTION'].find_one({"_id": user_obj._id})
        if not user['isadmin'] == True:
            return False # user is not admin
        else:
            return True  # user is admin

