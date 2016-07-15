from flask.ext.login import LoginManager, current_user
from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from flask_mongoengine import MongoEngine
import logging
from momentjs import momentjs



app = Flask(__name__)            # init app
app.config.from_object('config') # read config.py

login_manager = LoginManager()                #init login-manager
login_manager.init_app(app)                   # set app
login_manager.login_view = 'login'            # set login view
login_manager.session_protection = "strong"   # set level protection
login_manager.refresh_view = "accounts.reauthenticate"
login_manager.needs_refresh_message = (
    u"To protect your account, please reauthenticate to access this page."
)
login_manager.needs_refresh_message_category = "info"


db  = MongoEngine(app)           # init mongoengine
#dtb = DebugToolbarExtension(app) # init debug object

# Enable logging with file
if app.config['LOG']:
   logging.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s', level = logging.DEBUG, filename = app.config['LOG']) #u'sitelog.log'
   logging.info( u'Start server' ) # add log event

# register blueprint objects
def register_blueprints(app):
    from views import posts
    from admin import admin, user

    app.register_blueprint(posts)
    app.register_blueprint(admin)
    app.register_blueprint(user)

# perform register
register_blueprints(app)


if __name__ == '__main__':
    app.run()
