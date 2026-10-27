from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# n8n Webhook URL
N8N_WEBHOOK_URL = "http://localhost:5678/webhook/login"

@app.route('/send-to-n8n', methods=['POST'])
def send_to_n8n():

    # Get data from the API request
    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "No JSON data received"
        }), 400

    try:
        # Send data from Flask API to n8n
        response = requests.post(
            N8N_WEBHOOK_URL,
            json=data
        )

        # Check n8n response
        if response.status_code == 200:
            return jsonify({
                "success": True,
                "message": "Data sent to n8n successfully",
                "n8n_response": response.json()
            }), 200

        else:
            return jsonify({
                "success": False,
                "message": "n8n returned an error",
                "status_code": response.status_code
            }), response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({
            "success": False,
            "message": "Could not connect to n8n",
            "error": str(e)
        }), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)

