from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from supabase import create_client
import os

app = Flask(__name__)
CORS(app)

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/submit", methods=["POST"])
def submit():
    content = request.json.get("content", "").strip()
    if not content:
        return jsonify({"error": "Empty"}), 400
    supabase.table("thoughts").insert({
        "content": content,
        "lang": request.json.get("lang", "unknown")
    }).execute()
    return jsonify({"ok": True})

@app.route("/thoughts", methods=["GET"])
def thoughts():
    data = supabase.table("thoughts").select("*").order("timestamp", desc=True).execute()
    return jsonify(data.data)

if __name__ == "__main__":
    app.run(debug=True)
