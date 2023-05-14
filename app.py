from flask import Flask, render_template, request, abort
from flask_sqlalchemy import SQLAlchemy
from config import USERNAME, PASSWORD, HOST, PORT, DATABASE

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'
db = SQLAlchemy(app)


@app.route('/')
def index():
    recipes = ['AAA', 'BBB', 'CCC', 'DDD', 'EEE', 'FFF']
    return render_template('pages/index.html', recipes=recipes)


@app.route('/ingredient_adjustment')
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
