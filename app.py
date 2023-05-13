from flask import Flask, render_template, request, redirect

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('pages/index.html')


@app.route('/add_row')
def add_row():
    row = request.args.get('row')
    return render_template('components/row.html', row=row)


if __name__ == '__main__':
    app.run()
