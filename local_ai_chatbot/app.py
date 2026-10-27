
from flask import Flask, request, jsonify, render_template, Response
import requests
import json

app = Flask(__name__)

# Local Ollama settings
OLLAMA_URL = "http://127.0.0.1:11434/api/chat"
MODEL = "llama3.2"

SYSTEM_PROMPT = """
You are Nova, a friendly and helpful AI assistant.
Explain things clearly and accurately.
Use simple language when appropriate.
For programming questions, provide correct code and explain it.
If you are unsure about an answer, say so honestly.
"""

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "success": False,
            "message": "Invalid JSON request."
        }), 400

    # Accept either conversation history or a single message.
    messages = data.get("messages")

    if messages is None:
        message = data.get("message", "")

        if not isinstance(message, str) or not message.strip():
            return jsonify({
                "success": False,
                "message": "Please enter a message."
            }), 400

        messages = [{
            "role": "user",
            "content": message.strip()
        }]

    if not isinstance(messages, list) or not messages:
        return jsonify({
            "success": False,
            "message": "Please send a valid conversation."
        }), 400

    if len(messages) > 80:
        return jsonify({
            "success": False,
            "message": "The conversation is too long. Start a new chat."
        }), 400

    # Validate and prepare conversation history.
    clean_messages = [{
        "role": "system",
        "content": SYSTEM_PROMPT
    }]

    for item in messages:
        if not isinstance(item, dict):
            return jsonify({
                "success": False,
                "message": "Invalid message format."
            }), 400

        role = item.get("role")
        content = item.get("content")

        if role not in ("user", "assistant"):
            return jsonify({
                "success": False,
                "message": "Invalid message role."
            }), 400

        if not isinstance(content, str):
            return jsonify({
                "success": False,
                "message": "Message content must be text."
            }), 400

        if content.strip():
            clean_messages.append({
                "role": role,
                "content": content.strip()
            })

    if (
        len(clean_messages) < 2
        or clean_messages[-1]["role"] != "user"
    ):
        return jsonify({
            "success": False,
            "message": "Please send a new question."
        }), 400

    # Connect to Ollama. Streaming lets the browser show
    # the answer as the model generates it.
    try:
        upstream = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "messages": clean_messages,
                "stream": True,
                "keep_alive": "10m",
                "options": {
                    "temperature": 0.7
                }
            },
            stream=True,
            timeout=(10, 300)
        )

        if not upstream.ok:
            try:
                details = upstream.json().get(
                    "error", "Ollama returned an error."
                )
            except (ValueError, AttributeError):
                details = "Ollama returned an error."

            upstream.close()

            return jsonify({
                "success": False,
                "message": details
            }), 502

    except requests.exceptions.ConnectionError:
        return jsonify({
            "success": False,
            "message": (
                "Cannot connect to Ollama. "
                "Make sure Ollama is running on your computer."
            )
        }), 503

    except requests.exceptions.Timeout:
        return jsonify({
            "success": False,
            "message": "Ollama took too long to respond. Try again."
        }), 504

    except requests.exceptions.RequestException as error:
        app.logger.exception("Ollama request failed")

        return jsonify({
            "success": False,
            "message": "Could not contact Ollama: " + str(error)
        }), 502

    def generate():
        try:
            for line in upstream.iter_lines():
                if not line:
                    continue

                # requests may return bytes; decode them safely.
                if isinstance(line, bytes):
                    line = line.decode("utf-8", errors="replace")

                # Send one complete JSON line to the browser.
                yield line + "\n"

        except requests.exceptions.RequestException:
            app.logger.exception("Ollama streaming failed")

            yield json.dumps({
                "error": "The connection to Ollama was interrupted."
            }) + "\n"

        finally:
            upstream.close()

    return Response(
        generate(),
        mimetype="application/x-ndjson",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no"
        }
    )


@app.errorhandler(500)
def internal_server_error(error):
    app.logger.exception("Flask encountered an internal error")

    return jsonify({
        "success": False,
        "message": "An internal server error occurred. Check the Flask terminal."
    }), 500


if __name__ == "__main__":
    print("Nova AI Chatbot is starting...")
    print("Model:", MODEL)
    print("Open: http://127.0.0.1:5000")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        threaded=True
    )


