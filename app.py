import os
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
        print("✅ POST request received at /submit")
        print("Raw form data:", request.form)

        email = request.form.get("email")
        print(f"➡️ Email received: {email}")

        return jsonify({"status": "success", "message": "Form submitted successfully"}), 200

    except Exception as e:
        print("❌ Error:", e)
        return jsonify({"status": "error", "message": "Error processing form"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render sets PORT dynamically
    app.run(debug=False, host="0.0.0.0", port=port)
