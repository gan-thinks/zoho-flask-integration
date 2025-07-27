import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Function to get a fresh Zoho access token
def get_access_token():
    url = "https://accounts.zoho.in/oauth/v2/token"
    data = {
        "refresh_token": os.getenv("ZOHO_REFRESH_TOKEN"),
        "client_id": os.getenv("ZOHO_CLIENT_ID"),
        "client_secret": os.getenv("ZOHO_CLIENT_SECRET"),
        "grant_type": "refresh_token"
    }
    response = requests.post(url, data=data)
    response.raise_for_status()
    return response.json()["access_token"]

# Route to receive form submissions from Webflow and push to Zoho
@app.route('/submit', methods=['POST'])
def submit_to_zoho():
    try:
        # Get access token
        access_token = get_access_token()

        # Get form data (from Webflow form)
        form_data = request.form

        # Construct Zoho Lead payload
        lead_data = {
            "data": [
                {
                    "Company": form_data.get("company", "Webflow Lead"),
                    "Last_Name": form_data.get("last_name", "Unknown"),
                    "First_Name": form_data.get("first_name", ""),
                    "Email": form_data.get("email", ""),
                    "Phone": form_data.get("phone", "")
                }
            ]
        }

        # Zoho API endpoint
        url = f"{os.getenv('ZOHO_API_DOMAIN')}/crm/v2/Leads"

        # Headers
        headers = {
            "Authorization": f"Zoho-oauthtoken {access_token}",
            "Content-Type": "application/json"
        }

        # Send lead to Zoho
        response = requests.post(url, headers=headers, json=lead_data)

        if response.status_code == 201:
            return jsonify({"message": "Lead successfully created!"}), 201
        else:
            return jsonify({"error": response.json()}), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
