import base64
import configparser
import json
import os
import urllib.parse
from datetime import datetime, timedelta

from flask import Flask, render_template, request, abort, redirect, url_for, flash, Request
from flask_ckeditor import CKEditor
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
from hashids import Hashids
from werkzeug.security import generate_password_hash, check_password_hash

from forms import SignupForm, LoginForm, CKEditorForm
from models import db, User, Recipe, Followership, Like, Bookmark

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

db.init_app(app)
Migrate(app, db)
ckeditor = CKEditor(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = '請先登入'
login_manager.login_message_category = 'warning'


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


@login_manager.request_loader
def load_user_from_request(request: Request) -> User | None:
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


@app.template_filter('friendly_time')
def format_friendly_time(timestamp: datetime) -> str:
    diff = datetime.now() - timestamp
    if diff < timedelta(minutes=1):
        return f'{diff.seconds} 秒前'
    elif diff < timedelta(hours=1):
        return f'{diff.seconds // 60} 分鐘前'
    elif diff < timedelta(days=1):
        return f'{diff.seconds // 3600} 小時前'
    elif diff < timedelta(weeks=1):
        return f'{diff.days} 天前'
    else:
        return timestamp.strftime('%Y-%m-%d %H:%M:%S')


@app.route('/')
def index():
    public_recipes = Recipe.query.filter_by(public=True).order_by(Recipe.created_at.desc()).all()
    self_recipes = Recipe.query.filter_by(user_id=current_user.id).all() if current_user.is_authenticated else []
    bookmarked_recipes = db.session.query(Recipe) \
        .join(Bookmark, Recipe.id == Bookmark.recipe_id) \
        .filter_by(user_id=current_user.id, marked=True) \
        .all() if current_user.is_authenticated else []
    return render_template(
        'pages/index.html',
        public_recipes=public_recipes,
        self_recipes=self_recipes,
        bookmarked_recipes=bookmarked_recipes
    )


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
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
    if current_user.is_authenticated:
        return redirect(url_for('index'))
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


@app.route('/profile/<name>')
def profile(name):
    user = User.query.filter_by(name=name).first()
    if user:
        follower_count = Followership.query.filter_by(followed_id=user.id, following=True).count()
        if current_user.is_authenticated and user.id == current_user.id:
            recipes = Recipe.query.filter_by(user_id=user.id).order_by(Recipe.created_at.desc()).all()
        else:
            recipes = Recipe.query.filter_by(user_id=user.id, public=True).order_by(Recipe.created_at.desc()).all()
        following = current_user.is_authenticated and Followership.query.\
            filter_by(follower_id=current_user.id, followed_id=user.id, following=True).first() is not None
        return render_template(
            'pages/profile.html',
            user=user,
            following=following,
            follower_count=follower_count,
            recipes=recipes
        )
    else:
        flash('無此使用者', 'danger')
        return redirect(url_for('index'))


@app.route('/view_recipe/<token>')
@login_required
def view_recipe(token):
    recipe = Recipe.query.filter_by(token=token).first()
    if recipe:
        if not recipe.public and recipe.user_id != current_user.id:
            abort(401)
        ingredients = json.loads(urllib.parse.unquote(recipe.ingredients))
        like = Like.query.filter_by(user_id=current_user.id, recipe_id=recipe.id).first()
        liked_count = Like.query.filter_by(recipe_id=recipe.id, liked=True).count()
        bookmark = Bookmark.query.filter_by(user_id=current_user.id, recipe_id=recipe.id).first()
        return render_template(
            'pages/recipe.html',
            recipe=recipe,
            ingredients=ingredients,
            liked=like and like.liked,
            liked_count=liked_count,
            marked=bookmark and bookmark.marked
        )
    else:
        flash('無此食譜', 'danger')
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
        recipe = Recipe(
            user_id=current_user.id,
            title=form.title.data,
            ingredients=form.ingredients.data,
            instructions=form.instructions.data,
            public=form.public.data
        )
        db.session.add(recipe)
        db.session.commit()
        recipe.token = Hashids(salt="Recipizzazz", min_length=20).encode(recipe.id)
        db.session.commit()
        flash('發布成功', 'success')
        return redirect(url_for('index'))
    return render_template('pages/new-recipe.html', form=form)


@app.route('/add_recipe_row')
def add_recipe_row():
    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        abort(403)
    return render_template('components/recipe-row.html')


@app.route('/toggle_follow')
def toggle_follow():
    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        abort(403)
    following = request.args.get('following') == 'true'
    followed = User.query.filter_by(name=urllib.parse.unquote(request.args.get('followed_name'))).first()
    followership = Followership.query.filter_by(follower_id=current_user.id, followed_id=followed.id).first()
    if followership:
        followership.following = not following
        db.session.commit()
    else:
        followership = Followership(follower_id=current_user.id, followed_id=followed.id)
        db.session.add(followership)
        db.session.commit()
    return render_template('components/follow-button.html', following=not following)


@app.route('/toggle_like')
def toggle_like():
    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        abort(403)
    liked = request.args.get('liked') == 'true'
    liked_count = int(request.args.get('liked_count')) + (-1 if liked else 1)
    recipe = Recipe.query.filter_by(token=request.args.get('token')).first()
    like = Like.query.filter_by(user_id=current_user.id, recipe_id=recipe.id).first()
    if like:
        like.liked = not liked
        db.session.commit()
    else:
        like = Like(user_id=current_user.id, recipe_id=recipe.id)
        db.session.add(like)
        db.session.commit()
    return render_template('components/like-button.html', liked=not liked, liked_count=liked_count)


@app.route('/toggle_mark')
def toggle_mark():
    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        abort(403)
    marked = request.args.get('marked') == 'true'
    recipe = Recipe.query.filter_by(token=request.args.get('token')).first()
    bookmark = Bookmark.query.filter_by(user_id=current_user.id, recipe_id=recipe.id).first()
    if bookmark:
        bookmark.marked = not marked
        db.session.commit()
    else:
        bookmark = Bookmark(user_id=current_user.id, recipe_id=recipe.id)
        db.session.add(bookmark)
        db.session.commit()
    return render_template('components/mark-button.html', marked=not marked)


if __name__ == '__main__':
    app.run()
