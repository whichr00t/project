from flask import Flask, request, jsonify
import re
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow CORS for testing frontend on a different origin

# Define password strength rules
def check_password_strength(password):
    rules = [
        {"regex": r".{8,}", "message": "At least 8 characters long."},
        {"regex": r"[A-Z]", "message": "At least one uppercase letter."},
        {"regex": r"[a-z]", "message": "At least one lowercase letter."},
        {"regex": r"\d", "message": "At least one digit."},
        {"regex": r"[!@#$%^&*(),.?\":{}|<>]", "message": "At least one special character."},
        {"regex": r"^\S+$", "message": "No whitespace allowed."},
    ]

    issues = [rule["message"] for rule in rules if not re.search(rule["regex"], password)]
    return issues


# Route for home page
@app.route('/')
def home():
    return "Welcome to the Password Strength Checker API! Use the /check_password endpoint to test passwords."


# API to check password strength
@app.route('/check_password', methods=['POST'])
def check_password():
    data = request.json
    password = data.get("password")
    if not password:
        return jsonify({"success": False, "error": "Password is required"}), 400

    issues = check_password_strength(password)
    if not issues:
        return jsonify({"success": True, "message": "Password is strong!"})
    else:
        return jsonify({"success": False, "issues": issues})


# Route for favicon (to suppress browser warnings)
@app.route('/favicon.ico')
def favicon():
    return '', 204


if __name__ == '__main__':
    app.run(debug=True)
