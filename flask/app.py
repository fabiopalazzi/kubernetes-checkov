from flask import Flask, request, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://mongo.default.svc.cluster.local:27017/db"
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
    if data.get("title") is not None:
        inserted_note["title"] = data["title"]
    if data.get("body") is not None:
        inserted_note["body"] = data["body"]
    
    db.note.insert_one(inserted_note)

    return jsonify(
        message="note saved successfully!"
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)