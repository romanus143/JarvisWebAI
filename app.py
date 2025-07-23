# app.py
from flask_cors import CORS
CORS(app)

from flask import Flask, request, jsonify
from jarvis import JarvisCore  # assuming jarvis.py is in the same folder

app = Flask(__name__)
jarvis = JarvisCore()

@app.route("/")
def welcome():
    return "✅ Jarvis is online. Use POST /ask to talk to him."

@app.route("/ask", methods=["POST"])
def ask_jarvis():
    data = request.get_json()
    query = data.get("query", "")
    response = jarvis.respond(query)
    return jsonify({"response": response})

if __name__ == "__main__":
    import os
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)

