from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# Load Zoho OAuth token from environment
ZOHO_ACCESS_TOKEN = os.getenv("ZOHO_ACCESS_TOKEN")
ZOHO_API_URL = "https://www.zohoapis.in/crm/v2/Leads"

@app.route("/")
def index():
    return "✅ Flask server is running!"

@app.route("/webflow-form", methods=["POST"])
def handle_webflow_form():
    print("\n🔔 Webflow form submitted")

    data = request.form
    print("📥 Raw form data received:", data)

    # Extract fields (use field names exactly as in Webflow form `name` attributes)
    form_data = {
        "First_Name": data.get("first_name"),
        "Last_Name": data.get("last_name"),
        "Email": data.get("email"),
        "Chief_Health_Objective": data.get("chief_health_objective"),
        "Category_Resort": data.get("category_resort"),
        "Wish_to_Travel": data.get("wish_to_travel"),
        "Mobile": data.get("mobile_phone_number"),
        "Time_Wellness": data.get("time_wellness"),
        "Resort": data.get("resort"),
        "Visa": data.get("visa"),
        "Message": data.get("message")
    }

    # Remove any empty values
    clean_data = {k: v for k, v in form_data.items() if v}
    print("🧹 Cleaned form data:", clean_data)

    if not clean_data:
        print("⚠️ No valid form fields found.")
        return jsonify({"message": "No valid fields submitted"}), 400

    # Prepare data for Zoho CRM
    zoho_payload = {"data": [clean_data]}
    headers = {
        "Authorization": f"Zoho-oauthtoken {ZOHO_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    print("🚀 Sending data to Zoho CRM...")
    response = requests.post(ZOHO_API_URL, headers=headers, json=zoho_payload)

    print("📬 Zoho CRM Response Code:", response.status_code)
    print("📨 Zoho CRM Response Body:", response.text)

    if response.status_code == 201:
        print("✅ Successfully added to Zoho CRM")
        return "✅ Success from Flask!", 200
    else:
        print("❌ Failed to send to Zoho CRM")
        return jsonify({
            "message": "❌ Failed to add lead to Zoho CRM",
            "zoho_response": response.text
        }), 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Or use 10000 for local
    print(f"🚀 Starting Flask app on port {port}")
    app.run(host="0.0.0.0", port=port)
