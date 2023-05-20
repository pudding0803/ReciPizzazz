import base64
import os

from flask import Flask, render_template, request, abort, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash, check_password_hash

from config import USERNAME, PASSWORD, HOST, PORT, DATABASE
from models import db, User

app = Flask(__name__)
app.secret_key = os.urandom(32)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'

db.init_app(app)
Migrate(app, db)
csrf = CSRFProtect(app)

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
@csrf.exempt
def signup():
    if request.method == 'GET':
        return render_template('pages/signup.html')
    user = User(
        name=request.form.get('name'),
        account=request.form.get('account'),
        password=generate_password_hash(request.form.get('password'))
    )
    db.session.add(user)
    db.session.commit()
    login_user(user)
    flash('註冊成功', 'success')
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
@csrf.exempt
def login():
    if request.method == 'GET':
        return render_template('pages/login.html')
    user = User.query.filter_by(account=request.form.get('account')).first()
    if user and check_password_hash(user.password, request.form.get('password')):
        login_user(user)
        flash('登入成功', 'success')
        return redirect(url_for('index'))
    flash('帳號或密碼錯誤', 'danger')
    return render_template('pages/login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('已登出', 'info')
    return redirect(url_for('index'))


@app.route('/ingredient_adjustment')
@login_required
def ingredient_adjustment():
    return render_template('pages/ingredient-adjustment.html')


@app.route('/add_row')
def add_row():
    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        abort(403)
    row = request.args.get('row')
    return render_template('components/row.html', row=row)


@app.route('/toggle_lock')
def toggle_lock():
    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        abort(403)
    locked = request.args.get('locked') == 'true'
    return render_template('components/lock-button.html', locked=not locked)


if __name__ == '__main__':
    app.run()
