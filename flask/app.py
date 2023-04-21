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
    """
    Test simple route of flask
    """
    return '<h1>Hello from Flask</h2>'


@app.route('/test')
def testdb():
    """
    Test connection to mysql db
    """
    try:
        User.query.first()
        return '<h1>It works.</h1>'
    except Exception as e:
        print(str(e))
        return '<h1>Something is broken.</h1>'

##################
### user route ###
##################

@app.route("/user", methods=["GET"])
def get_all_users():
    """
    Return all users stored
    """
    users = User.query.all()
    items = [{
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "read": user.read if user.read is not None else "",
        "write": user.write if user.write is not None else "",
        "admin": user.admin if user.admin is not None else ""
    } for user in users]
    return jsonify(data=items)


@app.route("/user", methods=["POST"])
def add_users():
    """
    Add a new user with permissions
    """
    data = request.json
    if 'username' not in data or 'email' not in data:
        return jsonify({'message': 'Bad request!'}), 400
    username = data['username']
    email = data['email']
    read = data["read"] if 'read' in data and data['read'] is True else False
    write = data["write"] if 'write' in data and data['write'] is True else False
    admin = data["admin"] if 'admin' in data and data['admin'] is True else False

    try:
        new_user = User(username=username, email=email, read=read, write=write, admin=admin)
        db_mysql.session.add(new_user)
        db_mysql.session.commit()
    except Exception:
        return jsonify({'message': 'Error during adding user!'}), 500

    return jsonify({'message': 'User added successfully!'}), 201


@app.route("/user/<string:username>/permission", methods=["PUT"])
def set_permissions(username):
    """"
    Add permission to user identified by username param
    """
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({'message': 'User not found'}), 404

    data = request.json
    user.read = data["read"] if 'read' in data and data['read'] is True else False
    user.write = data["write"] if 'write' in data and data['write'] is True else False
    user.admin = data["admin"] if 'admin' in data and data['admin'] is True else False
    try:
        db_mysql.session.commit()
    except Exception:
        return jsonify({'message': 'Error during updating user!'}), 500

    return jsonify({'message': 'User updated successfully!'}), 201


@app.route("/user/<string:username>", methods=["DELETE"])
def delete_users(username):
    """
    Delete user identified by username query params
    """
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({'message': 'User not found'}), 404

    try:
        db_mysql.session.delete(user)
        db_mysql.session.commit()
    except Exception:
        return jsonify({'message': 'Error during adding user!'}), 500

    return jsonify({'message': 'User deleted successfully!'}), 202

##################
### note route ###
##################

@app.route("/note", methods=["GET"])
def get_all_notes():
    """
    Return all notes stored
    """
    username = request.args.get("username")
    # Check if user has permissions
    if username is None:
        return UnauthorizedResponse()
    user = User.query.filter_by(username=username).first()
    if user is None or user.read is False:
        return UnauthorizedResponse()
    # Get notes from mongo
    notes = db_mongo.note.find()
    items = [{
        "id": str(note["_id"]),
        "title": note["title"] if note.get("title") is not None else "",
        "body": note["body"] if note.get("body") is not None else "",
        "created_at": note["created_at"] if note.get("created_at") is not None else "",
        "created_by": note["created_by"] if note.get("created_by") is not None else "",
        "updated_at": note["updated_at"] if note.get("updated_at") is not None else ""
    } for note in notes]
    return jsonify(
        data=items
    )


@app.route("/note", methods=["POST"])
def create_note():
    """
    Create a new note specifying also username
    """
    data = request.get_json(force=True)

    # Check if user has permissions
    if data.get('username') is None:
        return UnauthorizedResponse()
    user = User.query.filter_by(username=data['username']).first()
    if user is None or user.write is False:
        return UnauthorizedResponse()
    # Manage note params
    inserted_note = {
        "created_at": str(datetime.now()),
        "created_by": data['username'],
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
    """
    Update note
    """
    data = request.get_json(force=True)

    # Check if user has permissions
    if data.get('username') is None:
        return UnauthorizedResponse()
    user = User.query.filter_by(username=data['username']).first()
    if user is None or user.admin is False:
        return UnauthorizedResponse()
    # Manage note params
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
    # Update note in mongo
    db_mongo.note.update_one({"_id": ObjectId(data.get("id"))}, {"$set": updated_note})

    return jsonify(
        message="note updated successfully!"
    )


@app.route("/note/<string:note_id>/", methods=["DELETE"])
def delete_note(note_id):
    """
    Delete note identified by note_id
    """
    username = request.args.get("username")
    # Check if user has permissions
    if username is None:
        return UnauthorizedResponse()
    user = User.query.filter_by(username=username).first()
    if user is None or user.admin is False:
        return UnauthorizedResponse()
    if note_id is None:
        return jsonify(
            message="Error, Id is not specified!"
        )
    # Delete note from mongo
    db_mongo.note.delete_one({"_id": ObjectId(note_id)})

    return jsonify(
        message="note deleted successfully!"
    )

def UnauthorizedResponse():
    return jsonify(
            message="Unauthorized!"
        ), 401

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)