import base64
import configparser
import os

from flask import Flask, render_template, request, abort, redirect, url_for, flash
from flask_ckeditor import CKEditor
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash

from forms import SignupForm, LoginForm, CKEditorForm
from models import db, User, Recipe

config = configparser.ConfigParser()
config.read('config.ini')

username = config.get('database', 'username')
password = config.get('database', 'password')
host = config.get('database', 'host')
port = config.getint('database', 'port')
database = config.get('database', 'database')

app = Flask(__name__)
app.secret_key = os.urandom(32)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{username}:{password}@{host}:{port}/{database}'
app.config['CKEDITOR_PKG_TYPE'] = 'basic'
ckeditor = CKEditor(app)

db.init_app(app)
Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = '請先登入'
login_manager.login_message_category = 'warning'


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


@login_manager.request_loader
def load_user_from_request(request):
    api_key = request.args.get('api_key')
    if api_key:
        user = User.query.filter_by(api_key=api_key).first()
        if user:
            return user
    api_key = request.headers.get('Authorization')
    if api_key:
        api_key = api_key.replace('Basic ', '', 1)
        try:
            api_key = base64.b64decode(api_key)
        except TypeError:
            pass
        user = User.query.filter_by(api_key=api_key).first()
        if user:
            return user
    return None


@app.route('/')
def index():
    recipes = ['AAA', 'BBB', 'CCC', 'DDD', 'EEE', 'FFF']
    return render_template('pages/index.html', recipes=recipes)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        if form.password.data != form.confirm_password.data:
            flash('輸入的密碼與確認密碼不相同', 'danger')
            return render_template('pages/signup.html', form=form)
        if User.query.filter(User.name == form.name.data).first() is not None:
            flash('此名稱已被使用', 'danger')
            return render_template('pages/signup.html', form=form)
        if User.query.filter(User.account == form.account.data).first() is not None:
            flash('此帳號已被使用', 'danger')
            return render_template('pages/signup.html', form=form)
        user = User(
            name=form.name.data,
            account=form.account.data,
            password=generate_password_hash(form.password.data)
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('註冊成功', 'success')
        return redirect(url_for('index'))
    return render_template('pages/signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(account=form.account.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('登入成功', 'success')
            return redirect(url_for('index'))
        flash('帳號或密碼錯誤', 'danger')
    return render_template('pages/login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('已登出', 'info')
    return redirect(url_for('index'))


@app.route('/ingredient_adjustment')
def ingredient_adjustment():
    return render_template('pages/ingredient-adjustment.html')


@app.route('/add_adjustment_row')
def add_adjustment_row():
    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        abort(403)
    row = request.args.get('row')
    return render_template('components/adjustment-row.html', row=row)


@app.route('/toggle_lock')
def toggle_lock():
    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        abort(403)
    locked = request.args.get('locked') == 'true'
    return render_template('components/lock-button.html', locked=not locked)


@app.route('/new_recipe', methods=['GET', 'POST'])
@login_required
def new_recipe():
    form = CKEditorForm()
    if form.validate_on_submit():
        # recipe = Recipe(
        #     user_id=current_user.id,
        #     title=form.title.data,
        #     ingredients=form.ingredients.data,
        #     contents=form.contents.data,
        #     public=form.public.data
        # )
        # db.session.add(recipe)
        # db.session.commit()
        flash('發布成功', 'success')
        return redirect(url_for('index'))
    return render_template('pages/new-recipe.html', form=form)


@app.route('/add_recipe_row')
def add_recipe_row():
    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        abort(403)
    return render_template('components/recipe-row.html')


if __name__ == '__main__':
    app.run()
