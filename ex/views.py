from flask import Blueprint, request, redirect, render_template, url_for, g, flash, current_app, send_from_directory
from flask.views import MethodView
from flask.ext.login import login_user, logout_user, login_required, current_user
from flask.ext.mongoengine.wtf import model_form
from ex import app,login_manager
from ex.models import Post, Comment, User
#from user import User
from forms import LoginForm
import logging
import os

posts = Blueprint('posts', __name__, template_folder='templates') #reg plueprint object

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


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()                                                              # init login form
    if request.method == 'POST' and form.validate_on_submit():                      # check method and form data
        user = app.config['USERS_COLLECTION'].find_one({"_id": form.username.data}) # find user by name
        if user and User.validate_login(user['password'], form.password.data):      # check user login and password
            user_obj = User(user['_id'])
            login_user(user_obj)
            g.user = user_obj
            flash("Logged in successfully!", category='success')
            logging.info(str(request.remote_addr) +u' - - User: ' + str(g.user._id) + u' "was login"')
            return redirect(request.args.get("next") or url_for("home"))
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

           if form.validate():
             comment = Comment()
             form.populate_obj(comment)

             post = context.get('post')
             post.comments.append(comment)

             post.save()

             return redirect(url_for('posts.detail', slug=slug))

           return render_template('posts/detail.html', **context)

# Register the urls
posts.add_url_rule('/', view_func=ListView.as_view('list'))
posts.add_url_rule('/<slug>/', view_func=DetailView.as_view('detail'))
