from flask import Flask, request, jsonify
from flask_cors import CORS
from jarvis import JarvisCore  # Assuming jarvis.py is in the same folder
import os

app = Flask(__name__)
CORS(app)  # ✅ Allows cross-origin requests from Netlify frontend

jarvis = JarvisCore()

@app.route("/")
def welcome():
    return "✅ Jarvis is online. Use POST /ask to talk to him."

@app.route("/ask", methods=["POST"])
def ask_jarvis():
    data = request.get_json()
    query = data.get("query", "").strip()

    if not query:
        return jsonify({ "response": "Please enter a question." })

    response = jarvis.respond(query)
    return jsonify({ "response": response or "Jarvis didn’t return anything." })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
