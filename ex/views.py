from flask import Blueprint, request, redirect, render_template, url_for, g, flash, current_app, send_from_directory, \
                        abort, session
from flask.views import MethodView
from flask.ext.login import login_user, logout_user, login_required, current_user, user_needs_refresh
from flask.ext.mongoengine.wtf import model_form
from ex import app,login_manager
from ex.models import Post, Comment, User
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, EditForm
from datetime import datetime
import logging
import os
import re

posts = Blueprint('posts', __name__, template_folder='templates') #reg plueprint object
global login_times
global login_ip

@app.errorhandler(404)
def not_found(error):
        return render_template('404.html'), 404

# for downloading sitelog.site - statistics
@app.route('/downloads/<filename>', methods=['GET', 'POST'])
@login_required
def download(filename):
    downloads = os.path.join(current_app.root_path, app.config['DOWNLOAD_FOLDER'])
    logging.info(str(request.remote_addr)+u' - - User: ' + str(g.user._id) + u' "Downloading log-file"')  # add log event
    return send_from_directory(directory=downloads, filename=filename)

login_times = 0
login_ip = ''

@app.route('/login', methods=['GET', 'POST'])
def login():
    global login_times
    global login_ip

    #bruteforce definition
    if login_ip == request.remote_addr: # check IP
        login_times += 1   # if one user then counter +1
    else:
        login_times = 0    # if enother user reset counter

    login_ip = request.remote_addr # save current IP

    if login_times>app.config['MAX_TRIES_TO_LOGIN']: # check counter
        login_times = 0                          # abort if > max times
        abort(403)

    form = LoginForm()                                                              # init login form
    if request.method == 'POST' and form.validate_on_submit():                      # check method and form data
        user = app.config['USERS_COLLECTION'].find_one({"_id": form.username.data}) # find user by name
        if user and User.validate_login(user['password'], form.password.data):      # check user login and password
            user_obj = User(user['_id'])                                            # get user object bi id from DB
            login_user(user_obj)                                                    # autorized the user
            g.user = user_obj                                                       # set global var to remember who was login
            login_times = 0                                                         # reset login counter
            g.user.add_stats("Loggined to site", datetime.utcnow(),request.referrer, str(request.remote_addr))
            flash("Logged in successfully!", category='success')                    # show message success comin
            logging.info(str(request.remote_addr) +u' - - User: ' + str(g.user._id) + u' "was login"') # add info to log-file
            return redirect(request.args.get("next") or url_for("home"))            # redirect to home page
        flash("Wrong username or password!", category='error')
    return render_template('login.html', title='login', form=form)          #rollback to login page



@app.route('/logout')
def logout():
    # logout from site
    logout_user()  
    return redirect(url_for('login'))



@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    # go to home page when loggined on main page
    return render_template('home.html')

#Set global var: g.user
@app.before_request
def before_request():
    # update global variable g.user
    g.user = current_user
    g.user.last_seen = datetime.utcnow()
    if g.user.is_anonymous == False:
       logging.info(str(request.remote_addr) + ' - - User: ' + str(g.user._id) + "Last seen at "+str(datetime.utcnow()))  # add log event 

    # session counter for reset timeout
    try:
        session['counter'] += 1
    except KeyError:
        session['counter'] = 1


# Load user from DB
@login_manager.user_loader
def load_user(username):
    u = app.config['USERS_COLLECTION'].find_one({"_id": username}) # find user by username in DB
    if not u:
        return None
    return User(u['_id'])

# Load and render list of articles
class ListView(MethodView):
    def get(self):
        session.permanent = True
        posts = Post.objects.all()
        return render_template('posts/list.html', posts=posts)

# Show article
class DetailView(MethodView):
    form = model_form(Comment, exclude=['created_at'])
    def get_context(self, slug):
        post = Post.objects.get_or_404(slug=slug)
        form = self.form(request.form)

        context = {
            "post": post,
            "form": form
        }
        return context

    def get(self, slug):
        post = Post.objects.get_or_404(slug=slug)
        return render_template('posts/detail.html', post=post)

    @login_required
    def post(self, slug):
           context = self.get_context(slug)
           form = context.get('form')
           form.author.data = g.user._id

           if form.validate():
             comment = Comment()

             form.populate_obj(comment)

             post = context.get('post')
             post.comments.append(comment)

             post.save()

             return redirect(url_for('posts.detail', slug=slug))

           return render_template('posts/detail.html', **context)

class UserProfile(MethodView):

        """ Class for view user profile """

        @login_required
        def get_context(self, nikname=None):            
            if nikname:  # when edit user
                form_cls = EditForm() 
                user_data = app.config['USERS_COLLECTION'].find_one({"_id": nikname})

                user = User()

                user._id = user_data['_id']
                user.login = user_data['login']
                user.address = user_data['address']
                user.firstname = user_data['firstname']
                user.password = user_data['password']
                user.secondname = user_data['secondname']
                user.isadmin = user_data['isadmin']
                user.email = user_data['email']
                user.about = user_data['about']
                
                
                                
                if request.method == 'POST':
                    user.address = form_cls.address.data
                    user.firstname = form_cls.firstname.data
                    user.secondname = form_cls.secondname.data
                    user.isadmin = form_cls.isadmin.data
                    user.about = form_cls.about.data
                    
                    # Checing e-mail
                    if re.search(r'@', form_cls.email.data):
                        user.email = form_cls.email.data
                    else:
                        flash("Please check youre e-mail", category='error')
                        return 0 
                        
                    #Checking password    
                    if form_cls.newpassword1.data and form_cls.newpassword2.data:
                        if form_cls.newpassword1.data == form_cls.newpassword2.data:
                            if check_password_hash(user.password, form_cls.oldpassword.data):
                                user.password = generate_password_hash(form_cls.newpassword1.data, method='pbkdf2:sha256')
                                user_needs_refresh # refresh session data
                            else:
                                flash("Please check youre old password", category='error')
                                return 0
                        else:
                            flash("Please retype new password 2 times correctly", category='error')
                            return 0

                else:

                    form_cls.address.data = user.address
                    form_cls.firstname.data = user.firstname
                    form_cls.secondname.data = user.secondname
                    form_cls.email.data = user.email
                    form_cls.oldpassword.data = ''
                    form_cls.newpassword1.data = ''
                    form_cls.newpassword2.data = ''
                    form_cls.isadmin.data = user.isadmin
                    form_cls.about.data = user.about

            context = {
                "user": user,
                "form": form_cls, 
                "create": nikname is None
            }
            return context

        @login_required
        def get(self, nikname):
            # define another login edit
            if not nikname == g.user._id:
                  abort(404)
            context = self.get_context(nikname)
            return render_template('user.html', **context)

        @login_required
        def post(self, nikname):
            context = self.get_context(nikname)
            if not context == 0:
                form = context.get('form')

                if form.validate():
                    user = context.get('user')

                    if user._id == None:  # When this is new er
                        user.password = generate_password_hash(user.password, method='pbkdf2:sha256')

                    if not user._id == user.login:
                        try:
                            app.config['USERS_COLLECTION'].delete_one({"_id": user._id})  # delete old document by id
                        except:
                           flash("There were some mistake, when we tried to delete the user " + user._id, category='error')
                        user._id = user.login  # change _id - this make method 'save' to insert mode
                    try:
                     user.save()
                    except:
                        flash("There were some mistake, when we tried to save youre profile " + user._id, category='error')
                    return  redirect(url_for('posts.list'))
                return render_template('user.html', **context)
            return redirect(url_for('posts.profile', nikname = nikname))
        
# Register the urls
posts.add_url_rule('/', view_func=ListView.as_view('list'))
posts.add_url_rule('/<slug>/', view_func=DetailView.as_view('detail'))
posts.add_url_rule('/profile/<nikname>/', view_func=UserProfile.as_view('profile'))
