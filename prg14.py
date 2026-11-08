# Import Flask and jsonify
from flask import Flask, jsonify

# Create the Flask application
app = Flask(__name__)

# Home route
@app.route("/", methods=["GET"])
def home():

    # Return a success message
    return jsonify({
        "success": True,
        "status": "success",
        "message": "Flask API is running successfully"
    }), 200


# API endpoint to retrieve data
@app.route("/api/data", methods=["GET"])
def get_data():

    # Return data in JSON format
    return jsonify({
        "success": True,
        "status": "success",
        "message": "Data retrieved successfully",
        "data": {
            "id": 1,
            "name": "Sample Data"
        }
    }), 200


# Handle invalid API endpoints
@app.errorhandler(404)
def not_found(error):

    # Return a 404 error message
    return jsonify({
        "success": False,
        "status": "error",
        "message": "Endpoint not found"
    }), 404


# Run the Flask application locally
if __name__ == "__main__":
    app.run(debug=True)
