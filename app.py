from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

ZOHO_ACCESS_TOKEN = os.getenv("ZOHO_ACCESS_TOKEN")
ZOHO_API_URL = "https://www.zohoapis.in/crm/v2/Leads"

@app.route('/webflow-form', methods=['POST'])
def handle_webflow_form():
    data = request.form

    # Extract all fields from Webflow form
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

    # Remove None values to avoid errors
    clean_data = {k: v for k, v in form_data.items() if v is not None}

    zoho_payload = {
        "data": [clean_data]
    }

    headers = {
        "Authorization": f"Zoho-oauthtoken {ZOHO_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    response = requests.post(ZOHO_API_URL, headers=headers, json=zoho_payload)

    if response.status_code == 201:
        return jsonify({"message": "Lead successfully added to Zoho CRM"}), 201
    else:
        return jsonify({
            "message": "Failed to add lead",
            "zoho_response": response.text
        }), 400

if __name__ == '__main__':
    app.run(debug=True)
