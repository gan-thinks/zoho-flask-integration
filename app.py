from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route("/", methods=["GET"])
def home():
    return "Flask server is live!"

@app.route("/submit", methods=["POST"])
def submit_form():
    try:
        print("✅ Received a POST request to /submit")

        # Log raw data
        print("Raw form data:", request.form)

        # Extract form data
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        message = request.form.get("message")

        print(f"Parsed Form Data ➡️ Name: {name}, Email: {email}, Phone: {phone}, Message: {message}")

        # You can do something here like send to Zoho CRM

        # Webflow needs a 200 response to show success message
        return jsonify({"status": "success", "message": "Form submitted successfully ✅"}), 200

    except Exception as e:
        print("❌ Error while processing form:", str(e))
        return jsonify({"status": "error", "message": "Something went wrong!"}), 500

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=10000)
