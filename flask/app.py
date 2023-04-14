import os
from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.sql import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@mysql-svc.checkov-project.svc.cluster.local:3306' \
                                        '/mydatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    read = db.Column(db.Boolean, default=False)
    write = db.Column(db.Boolean, default=False)
    admin = db.Column(db.Boolean, default=False)

    def __int__(self, id, username, email, read, write, admin):
        self.id = id
        self.username = username
        self.email = email
        self.read = read
        self.write = write
        self.admin = admin


with app.app_context():
    db.create_all()


@app.route('/')
def hello_geek():
    return '<h1>Ciao</h2>'


@app.route('/test')
def testdb():
    try:
        User.query.filter_by(username=3).all()
        return '<h1>It works.</h1>'
    except Exception as e:
        print(str(e))
        return '<h1>Something is broken.</h1>'


@app.route("/users", methods=["GET"])
def get_all_users():
    users = User.query.all()
    data = []
    for user in users:
        item = {
            "id": user.id,
            "username": user.username if user.username is not None else "",
            "email": user.email if user.email is not None else "",
            "read": user.read if user.read is not None else "",
            "write": user.write if user.write is not None else "",
            "admin": user.admin if user.admin is not None else ""
        }
        data.append(item)
    return jsonify(data=data)


@app.route("/add_users", methods=["POST"])
def add_users():
    username = request.json['username']
    email = request.json['email']
    read = request.json["read"]
    write = request.json["write"]
    admin = request.json["admin"]

    new_user = User(username=username, email=email, read=read, write=write, admin=admin)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User added successfully!'}), 201


@app.route("/set_permissions/<string:username>", methods=["PUT"])
def set_permissions(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({'message': 'User not found'}), 404

    data = request.json
    user.read = data["read"] if "read" in data else user.read
    user.write = data["write"] if "write" in data else user.write
    user.admin = data["admin"] if "admin" in data else user.admin

    db.session.commit()

    return jsonify({'message': 'User updated successfully!'}), 201


@app.route("/delete_users/<string:username>", methods=["DELETE"])
def delete_users(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({'message': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'User deleted successfully!'}), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
