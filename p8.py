from flask import Flask, request, jsonify
app = Flask(__name__)
VALID_USERNAME = "admin"
VALID_PASSWORD = "password123"

# ---------------- GET METHOD ----------------
@app.route('/login', methods=['GET'])
def get_login():

    return jsonify({
        "message": "Login API is working"
    })


# ---------------- POST METHOD ----------------
@app.route('/login', methods=['POST'])
def post_login():

    data = request.get_json()

    username = data.get('username', '')
    password = data.get('password', '')

    if username == VALID_USERNAME and password == VALID_PASSWORD:

        return jsonify({
            "success": True,
            "message": "Login successful"
        })

    else:

        return jsonify({
            "success": False,
            "message": "Invalid username or password"
        }), 401


# ---------------- RUN APPLICATION ----------------
if __name__ == '__main__':
    app.run(debug=True)