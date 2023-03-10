from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@mysql-deployment:3306/mydatabase'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)


@app.route('/')
def hello_geek():
    return '<h1>Dai Inter vinci per noi</h2>'


if __name__ == '__main__':
    app.run(debug=True)
