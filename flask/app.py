from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime
import os
from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.sql import func

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://mongodb-service." + os.environ['NAMESPACE'] + ".svc.cluster.local:27017/db"
mongo = PyMongo(app)
db_mongo = mongo.db

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@mysql-svc.checkov-project.svc.cluster.local:3306' \
                                        '/mydatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db_mysql = SQLAlchemy(app)


class User(db_mysql.Model):
    __tablename__ = 'users'
    id = db_mysql.Column(db_mysql.Integer, primary_key=True)
    username = db_mysql.Column(db_mysql.String(80), unique=True, nullable=False)
    email = db_mysql.Column(db_mysql.String(120), unique=True, nullable=False)
    read = db_mysql.Column(db_mysql.Boolean, default=False)
    write = db_mysql.Column(db_mysql.Boolean, default=False)
    admin = db_mysql.Column(db_mysql.Boolean, default=False)

    def __int__(self, id, username, email, read, write, admin):
        self.id = id
        self.username = username
        self.email = email
        self.read = read
        self.write = write
        self.admin = admin


with app.app_context():
    db_mysql.create_all()


@app.route('/')
def hello_geek():
    return '<h1>Hello from Flask</h2>'


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
    db_mysql.session.add(new_user)
    db_mysql.session.commit()

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

    db_mysql.session.commit()

    return jsonify({'message': 'User updated successfully!'}), 201


@app.route("/delete_users/<string:username>", methods=["DELETE"])
def delete_users(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({'message': 'User not found'}), 404

    db_mysql.session.delete(user)
    db_mysql.session.commit()

    return jsonify({'message': 'User deleted successfully!'}), 201


@app.route("/notes", methods=["GET"])
def get_all_notes():
    notes = db_mongo.note.find()
    data = []
    for note in notes:
        item = {
            "id": str(note["_id"]),
            "title": note["title"] if note.get("title") is not None else "",
            "body": note["body"] if note.get("body") is not None else "",
            "created_at": note["created_at"] if note.get("created_at") is not None else "",
            "updated_at": note["updated_at"] if note.get("updated_at") is not None else ""
        }
        data.append(item)
    return jsonify(
        data=data
    )


@app.route("/note", methods=["POST"])
def create_note():
    data = request.get_json(force=True)
    inserted_note = {
        "created_at": str(datetime.now()),
        "updated_at": None
    }
    empty = True
    if data.get("title") is not None:
        empty = False
        inserted_note["title"] = data["title"]
    if data.get("body") is not None:
        empty = False
        inserted_note["body"] = data["body"]

    if empty:
        return jsonify(
            message="note is empty!"
        )

    db_mongo.note.insert_one(inserted_note)
    return jsonify(
        message="note saved successfully!"
    )


@app.route("/note", methods=["PUT"])
def update_note():
    data = request.get_json(force=True)
    updated_note = {
        "updated_at": str(datetime.now())
    }

    if data.get("id") is None:
        return jsonify(
            message="Error, Id is not specified!"
        )

    empty = True
    if data.get("title") is not None:
        empty = False
        updated_note["title"] = data["title"]
    if data.get("body") is not None:
        empty = False
        updated_note["body"] = data["body"]

    if empty:
        return jsonify(
            message="note is empty!"
        )

    db_mongo.note.update_one({"_id": ObjectId(data.get("id"))}, {"$set": updated_note})

    return jsonify(
        message="note updated successfully!"
    )


@app.route("/note", methods=["DELETE"])
def delete_note():
    id = request.args.get("id")
    if id is None:
        return jsonify(
            message="Error, Id is not specified!"
        )

    db_mongo.note.delete_one({"_id": ObjectId(id)})

    return jsonify(
        message="note deleted successfully!"
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
