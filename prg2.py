from flask import Flask, request, jsonify
import re

app = Flask(__name__)

# Regular expression for basic email validation
EMAIL_REGEX = r'^[\w\.-]+@[\w\.-]+\.\w+$'

@app.route('/register', methods=['POST'])
def register():
    # 1. Parse the incoming JSON data
    data = request.get_json()
    
    # Check if JSON payload exists
    if not data:
        return jsonify({"error": "Invalid request format. JSON expected."}), 400

    name = data.get('name', '').strip()
    email = data.get('email', '').strip()

    # 2. Scenario: Missing fields
    if not name or not email:
        return jsonify({"error": "Both 'name' and 'email' are required fields."}), 400

    # 3. Scenario: Invalid email
    if not re.match(EMAIL_REGEX, email):
        return jsonify({"error": "Invalid email format."}), 400

    # 4. Scenario: Valid email and successful registration
    # In a real app, you would save this to a database here
    return jsonify({
        "message": "Registration successful!",
        "user": {
            "name": name,
            "email": email
        }
    }), 201

if __name__ == '__main__':
    # This starts the Werkzeug development server on http://127.0.0.1:5000
    app.run(debug=True)


