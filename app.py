
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

OLLAMA_URL = "http://127.0.0.1:11434/api/chat"
MODEL = "llama3.2"

SYSTEM_MESSAGE = """
You are a helpful AI assistant.
Answer clearly and accurately.
Explain programming concepts step by step for beginners.
If you are unsure about an answer, say so.
"""

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    messages = data.get("messages", [])

    if not isinstance(messages, list) or not messages:
        return jsonify({
            "success": False,
            "error": "Please enter a message."
        }), 400

    clean_messages = []

    for item in messages[-12:]:
        if not isinstance(item, dict):
            continue

        role = item.get("role")
        content = item.get("content")

        if (
            role in ("user", "assistant")
            and isinstance(content, str)
            and content.strip()
        ):
            clean_messages.append({
                "role": role,
                "content": content.strip()[:6000]
            })

    if (
        not clean_messages
        or clean_messages[-1]["role"] != "user"
    ):
        return jsonify({
            "success": False,
            "error": "Please enter your question again."
        }), 400

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_MESSAGE}
        ] + clean_messages,
        "stream": False
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=180
        )

        if response.status_code == 404:
            return jsonify({
                "success": False,
                "error": "Model not found. Run: ollama pull llama3.2"
            }), 503

        response.raise_for_status()
        result = response.json()

        answer = result.get("message", {}).get("content", "").strip()

        if not answer:
            return jsonify({
                "success": False,
                "error": "The AI returned an empty answer."
            }), 502

        return jsonify({
            "success": True,
            "status": "success",
            "reply": answer
        })

    except requests.exceptions.ConnectionError:
        return jsonify({
            "success": False,
            "status": "error",
            "error": "Ollama is not running. Open the Ollama app."
        }), 503

    except requests.exceptions.Timeout:
        return jsonify({
            "success": False,
            "status": "error",
            "error": "The AI took too long. Please try again."
        }), 504

    except requests.exceptions.RequestException:
        return jsonify({
            "success": False,
            "status": "error",
            "error": "Could not get a response from Ollama."
        }), 502


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )
