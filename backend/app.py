from flask import Flask, request, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)

DB_FILE = "thoughts.json"

def load_thoughts():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_thought(thought):
    data = load_thoughts()
    data.append(thought)
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)

@app.route("/submit", methods=["POST"])
def submit():
    content = request.json.get("content", "").strip()

    if not content:
        return jsonify({"error": "Empty"}), 400

    thought = {
        "content": content,
        "timestamp": datetime.utcnow().isoformat()
    }

    save_thought(thought)

    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(debug=True)
