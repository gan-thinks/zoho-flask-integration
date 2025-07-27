from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Load Zoho OAuth token from environment
ZOHO_ACCESS_TOKEN = os.getenv("ZOHO_ACCESS_TOKEN")
ZOHO_API_URL = "https://www.zohoapis.in/crm/v2/Leads"

@app.route('/')
def index():
    return "Flask server is running!"

@app.route('/webflow-form', methods=['POST'])
def handle_webflow_form():
    print("✅ Webflow form submitted")

    data = request.form
    print("📥 Raw form data received:", data)

    # Extract fields (Make sure names match the Webflow input `name` attributes)
    form_data = {
        "First_Name": data.get("first-name"),
        "Last_Name": data.get("last-name"),
        "Email": data.get("email"),
        "Chief_Health_Objective": data.get("chief-health-objective"),
        "Category_Resort": data.get("category-resort"),
        "Wish_to_Travel": data.get("wish-to-travel"),
        "Mobile": data.get("mobile-phone-number"),
        "Time_Wellness": data.get("time-wellness"),
        "Resort": data.get("resort"),
        "Visa": data.get("visa"),
        "Message": data.get("message")
    }

    # Clean up None values
    clean_data = {k: v for k, v in form_data.items() if v}
    print("🧹 Cleaned form data:", clean_data)

    if not clean_data:
        print("⚠️ No valid form fields found")
        return jsonify({"message": "No valid fields submitted"}), 400

    # Prepare Zoho CRM payload
    zoho_payload = {"data": [clean_data]}
    headers = {
        "Authorization": f"Zoho-oauthtoken {ZOHO_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    print("📤 Sending data to Zoho CRM...")
    response = requests.post(ZOHO_API_URL, headers=headers, json=zoho_payload)

    print("📬 Zoho response:", response.status_code, response.text)

    if response.status_code == 201:
       return "Success from Flask!", 200

    else:
        return jsonify({
            "message": "❌ Failed to add lead to Zoho CRM",
            "zoho_response": response.text
        }), 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
