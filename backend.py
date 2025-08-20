# backend.py

from flask import Flask, request, jsonify
from detector import detect_fake_news

app = Flask(__name__)

@app.route("/check_news", methods=["POST"])
def check_news():
    data = request.json
    headline = data.get("headline", "")
    if not headline:
        return jsonify({"error": "No headline provided"}), 400

    verdict, sources = detect_fake_news(headline)
    return jsonify({"verdict": verdict, "sources": sources})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
