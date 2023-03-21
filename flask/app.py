import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.sql import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@mysql-svc.default.svc.cluster.local:32000/mydatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __int__(self, username, email):
        self.username = username
        self.email = email


@app.route('/test')
def testdb():
    try:
        db.session.query(User).all()
        return '<h1>It works.</h1>'
    except Exception as e:
        print(str(e))
        return '<h1>Something is broken.</h1>'


@app.route("/users", methods=["GET"])
def get_all_notes():
    users = db.db.query(User).all()
    data = []
    for user in users:
        item = {
            "id": user[0],
            "title": user[1] if user[1] is not None else "",
            "body": user[2] if user[2] is not None else ""
        }
        data.append(item)
    return jsonify(data=data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
