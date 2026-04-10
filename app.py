from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from datetime import datetime
import json
import os

app = Flask(__name__)
CORS(app)

DB_FILE = "thoughts.json"

def load_thoughts():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_thought(thought):
    data = load_thoughts()
    data.append(thought)
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/submit", methods=["POST"])
def submit():
    content = request.json.get("content", "").strip()
    if not content:
        return jsonify({"error": "Empty"}), 400
    thought = {
        "content": content,
        "timestamp": datetime.utcnow().isoformat(),
        "lang": request.json.get("lang", "unknown")
    }
    save_thought(thought)
    return jsonify({"ok": True})

@app.route("/thoughts", methods=["GET"])
def thoughts():
    return jsonify(load_thoughts())

if __name__ == "__main__":
    app.run(debug=True)
