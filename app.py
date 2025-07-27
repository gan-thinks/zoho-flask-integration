import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return "🚀 Flask server is live!"

@app.route("/submit", methods=["POST"])
def submit_form():
    print("🚨 Request received at /submit")
    print("➡️ Method:", request.method)
    print("➡️ Headers:", request.headers)

    try:
        # Check form-data
        if request.form:
            print("✅ Form data received:")
            for key in request.form:
                print(f"  - {key}: {request.form[key]}")
        else:
            print("⚠️ No form-data received")

        # Check JSON body
        data = request.get_json(silent=True)
        if data:
            print("✅ JSON data received:")
            for key in data:
                print(f"  - {key}: {data[key]}")
        else:
            print("⚠️ No JSON data received")

        # Extract example field (email)
        email = request.form.get("email") or (data or {}).get("email")
        print(f"📩 Email captured: {email}")

        return jsonify({"status": "success", "message": "Form submitted successfully"}), 200

    except Exception as e:
        print("❌ Exception occurred:", e)
        return jsonify({"status": "error", "message": "Something went wrong"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Use Render's port if set
    print(f"🌐 Running on port: {port}")
    app.run(debug=True, host="0.0.0.0", port=port)
