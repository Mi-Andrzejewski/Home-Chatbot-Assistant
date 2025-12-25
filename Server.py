#!/usr/bin/env python3
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

OLLAMA_API_URL = "127.0.0.1:11434"
OLLAMA_MODEL = "INSERT MODEL NAME HERE"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message")

    if not user_input:
        return jsonify({"error": "Brak wiadomości"}), 400

    payload = {
        "model": OLLAMA_MODEL,
        "messages": [
            {"role": "user", "content": user_input}
        ],
        "stream": False
    }

    try:
        response = requests.post("http://127.0.0.1:11434/api/chat", json=payload)
        response.raise_for_status()
        data = response.json()

        return jsonify({"response": data.get("message", {}).get("content", "Brak odpowiedzi")})

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Communication error with Ollama: {str(e)}"}), 500




if __name__ == ("__main__"):
    app.run(host="0.0.0.0", port=8000)
