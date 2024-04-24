import requests
import streamlit as st

def fetch_subscribers(access_token=None):
    """Fetch all active subscribers with their plan details."""
    if access_token is None:
        access_token = st.secrets["bmac_api_key"]
    url = "https://developers.buymeacoffee.com/api/v1/subscriptions"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()['data']
    else:
        raise Exception("Failed to fetch subscribers: {} - {}".format(response.status_code, response.text))

def is_subscriber_authorized(email, required_plan, subscribers):
    """Check if the provided email is subscribed to the required plan."""
    return any(sub['payer_email'] == email and sub['plan'] == required_plan for sub in subscribers)
