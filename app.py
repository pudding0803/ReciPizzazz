from flask import Flask, render_template, request, redirect, abort

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('pages/index.html')


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
