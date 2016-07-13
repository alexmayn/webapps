from flask.ext.mongoengine.wtf import model_form
from werkzeug.security import generate_password_hash
from ex.models import Post, User
#from ex.user import User
from auth import check_admin
from flask import Blueprint, request, redirect, render_template, url_for, g
from flask.views import MethodView
from flask.ext.login import logout_user, login_required
from ex import app


admin = Blueprint('admin', __name__, template_folder='templates')
user = Blueprint('user', __name__, template_folder='templates') #reg plueprint object

class List(MethodView):

    cls = Post

    @login_required
    def get(self):
        if check_admin():
          posts = self.cls.objects.all()
          return render_template('admin/list.html', posts=posts)
        return redirect(url_for('login', next='/admin')) #redirct to login?next=%2Fadmin%2F

class ListUsers(MethodView):

    cls = User

    @login_required
    def get(self):
        if check_admin():
            users = self.cls.objects.all() #show list users
            return render_template('admin/userlist.html', users=users)
        return redirect(url_for('login', next='/admin'))  # redirct to login?next=%2Fadmin%2F

class Admin(MethodView):

    @login_required
    def get(self):
        logout_user()
        return redirect(url_for('logout'))

class UserDetail(MethodView):

    @login_required
    def get_context(self, nikname=None):
        if nikname: # when edit user
            form_cls = model_form(User, only=('login', 'isadmin', 'address', 'firstname', 'secondname', 'email'))
            user_data = app.config['USERS_COLLECTION'].find_one({"_id": nikname})

            user = User()

            user._id =        user_data['_id']
            user.login =      user_data['login']
            user.address =    user_data['address']
            user.firstname =  user_data['firstname']
            user.password =   user_data['password']
            user.secondname = user_data['secondname']
            user.isadmin =    user_data['isadmin']
            user.email =      user_data['email']

            if request.method == 'POST':
                form = form_cls(request.form, inital=user._data)
            else:
                form = form_cls(obj=user)

        else: #When add new user
            form_cls = model_form(User)
            user = User()
            form = form_cls(request.form)

        context = {
            "user": user,
            "form": form,
            "create": nikname is None
        }
        return context

    @login_required
    def get(self, nikname):
        if request.method == 'DELETE':
            app.config['USERS_COLLECTION'].delete_one({"_id": nikname})  # delete old document by id
            return redirect(url_for('admin.users'))
        context = self.get_context(nikname)
        return render_template('admin/settings.html', **context)

    @login_required
 #   def delete(self, nikname):
 #       app.config['USERS_COLLECTION'].delete_one({"_id": nikname})  # delete old document by id
 #       return redirect(url_for('admin.users'))


    @login_required
    def post(self, nikname):
        context = self.get_context(nikname)
        form = context.get('form')

        if form.validate():
            user = context.get('user')
            form.populate_obj(user)

            if user._id == None: # When this is new er
                user.password = generate_password_hash(user.password , method='pbkdf2:sha256')

            if not user._id == user.login:
                try:
                   app.config['USERS_COLLECTION'].delete_one({"_id": user._id}) # delete old document by id
                except:
                   None
                user._id = user.login # change _id - this make method 'save' to insert mode
            try:
             user.save()
            except:
             None
            return redirect(url_for('admin.users'))
        return render_template('admin/settings.html', **context)




class Detail(MethodView):

    @login_required
    def get_context(self, slug=None):
        form_cls = model_form(Post, exclude=('created_at', 'comments'))

        if slug:
            post = Post.objects.get_or_404(slug=slug)
            if request.method == 'POST':
                form = form_cls(request.form, inital=post._data)
            else:
                form = form_cls(obj=post)
        else:
            post = Post()
            form = form_cls(request.form)

        context = {
            "post": post,
            "form": form,
            "create": slug is None
        }
        return context

    @login_required
    def get(self, slug):
        context = self.get_context(slug)
        return render_template('admin/detail.html', **context)

    @login_required
    def post(self, slug):
        context = self.get_context(slug)
        form = context.get('form')

        if form.validate():
            post = context.get('post')
            form.populate_obj(post)
            post.save()

            return redirect(url_for('admin.index'))
        return render_template('admin/detail.html', **context)



# Register the list of articles urls
admin.add_url_rule('/admin/', view_func=List.as_view('index'))
admin.add_url_rule('/admin/logout/', view_func=Admin.as_view('logout'))
admin.add_url_rule('/admin/create/', defaults={'slug': None}, view_func=Detail.as_view('create'))
admin.add_url_rule('/admin/<slug>/', view_func=Detail.as_view('edit'))
# Register users urls
admin.add_url_rule('/admin/users', view_func=ListUsers.as_view('users'))
admin.add_url_rule('/admin/useradd/', defaults={'nikname': None}, view_func=UserDetail.as_view('useradd'))
#admin.add_url_rule('/admin/userdelete/<nikname>',  view_func=UserDetail.as_view('userdelete'))
admin.add_url_rule('/admin/settings/<nikname>', view_func=UserDetail.as_view('settings'))

