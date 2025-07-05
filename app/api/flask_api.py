from flask import Flask, jsonify
import json
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load questions.json from ../app/data/questions.json
data_file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'questions.json')

with open(data_file_path, "r", encoding="utf-8") as f:
    questions = json.load(f)

# GET all questions
@app.route("/api/questions", methods=["GET"])
def get_all_questions():
    return jsonify(questions)

# GET questions by topic_id
@app.route("/api/questions/<topic_id>", methods=["GET"])
def get_questions_by_topic(topic_id):
    filtered_questions = [q for q in questions if q["topic_id"] == topic_id]
    return jsonify(filtered_questions)

# Health check
@app.route("/api/ping", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)