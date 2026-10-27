from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

VALID_USERNAME = "admin"
VALID_PASSWORD = "password123"

@app.route('/login', methods=['GET'])
def get_login():

    return render_template_string("""
        <h2>Login</h2>

        <form method="POST" action="/login">
            <input type="text" name="username" placeholder="Username">
            <br><br>

            <input type="password" name="password" placeholder="Password">
            <br><br>

            <button type="submit">Login</button>
        </form>
    """)
@app.route('/login', methods=['POST'])
def post_login():

    username = request.form.get('username', '')
    password = request.form.get('password', '')

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

if __name__ == '__main__':
    app.run(debug=True)