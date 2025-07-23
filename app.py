# app.py

from flask import Flask, request, jsonify
from jarvis import JarvisCore

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
    app.run(host="0.0.0.0", port=10000)
