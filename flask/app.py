from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import os

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://mongodb-service." + os.environ['NAMESPACE'] + ".svc.cluster.local:27017/db"
mongo = PyMongo(app)
db = mongo.db

@app.route('/')
def hello_geek():
    return '<h1>Hello from Flask & Docker & Kubernetes</h2>'

@app.route("/notes", methods=["GET"])
def get_all_notes():
    notes = db.note.find()
    data = []
    for note in notes:
        item = {
            "id": str(note["_id"]),
            "title": note["title"] if note.get("title") is not None else "",
            "body": note["body"] if note.get("body") is not None else ""
        }
        data.append(item)
    return jsonify(
        data=data
    )
@app.route("/note", methods=["POST"])
def create_note():
    data = request.get_json(force=True)
    inserted_note = {}
    empty = True
    if data.get("title") is not None:
        empty=False
        inserted_note["title"] = data["title"]
    if data.get("body") is not None:
        empty=False
        inserted_note["body"] = data["body"]
    
    if empty:
        return jsonify(
            message="note is empty!"
        )

    db.note.insert_one(inserted_note)
    return jsonify(
        message="note saved successfully!"
    )

@app.route("/note", methods=["PUT"])
def update_note():
    data = request.get_json(force=True)
    updated_note = {}

    if data.get("id") is None:
        return jsonify(
            message="Error, Id is not specified!"
        )

    empty = True
    if data.get("title") is not None:
        empty=False
        updated_note["title"] = data["title"]
    if data.get("body") is not None:
        empty=False
        updated_note["body"] = data["body"]
    
    if empty:
        return jsonify(
            message="note is empty!"
        )

    db.note.update_one({"_id": ObjectId(data.get("id"))}, {"$set": updated_note})

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

    db.note.delete_one({"_id": ObjectId(id)})

    return jsonify(
        message="note deleted successfully!"
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)