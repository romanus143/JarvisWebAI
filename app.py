from flask import Flask, request, jsonify
from flask_cors import CORS
from baba import BabaCore  # Make sure baba.py is in the same folder
import os

app = Flask(__name__)
# ✅ Supports cross-origin requests and handles preflight OPTIONS checks
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

baba = BabaCore()

@app.route("/")
def welcome():
    return "✅ Baba is online. Use POST /ask to talk to him."

@app.route("/ask", methods=["POST", "OPTIONS"])
def ask_baba():
    if request.method == "OPTIONS":
        return jsonify({}), 200  # Handles browser preflight check

    data = request.get_json()
    query = data.get("query", "").strip()

    if not query:
        return jsonify({ "response": "Please enter a question." })

    response = baba.respond(query)
    return jsonify({ "response": response or "Baba didn’t return anything." })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
