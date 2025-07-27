from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return "Flask server is live!"

@app.route("/submit", methods=["POST"])
def submit_form():
    try:
        print("✅ Received a POST request to /submit")
        print("📩 Raw form data:", request.form)

        # Only extract the email field
        email = request.form.get("email")
        print(f"📧 Received Email: {email}")

        # Return success response
        return jsonify({"status": "success", "message": "Email received ✅"}), 200

    except Exception as e:
        print("❌ Error while processing form:", str(e))
        return jsonify({"status": "error", "message": "Something went wrong!"}), 500

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=10000)
