import requests
import streamlit as st

def fetch_subscribers(access_token=None):
    """
    Fetch all active subscribers with their plan details.
    Handles API response and extracts necessary subscriber information.
    """
    if access_token is None:
        access_token = st.secrets["bmac_api_key"]
    
    url = "https://developers.buymeacoffee.com/api/v1/subscriptions"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        json_response = response.json()
        if 'data' in json_response:
            return json_response['data']
        else:
            st.error("Received unexpected data structure from BMAC API.")
            return []
    else:
        st.error(f"Failed to fetch subscribers: {response.status_code} - {response.text}")
        return []

def is_subscriber_authorized(email, subscribers):
    """
    Check if the provided email is present among the subscribers.
    Since plan data is not available, authorization is based on email presence alone.
    """
    for subscriber in subscribers:
        # Check if 'payer_email' is present and matches the given email
        if 'payer_email' in subscriber and subscriber['payer_email'] == email:
            # Additional checks can be added here based on other criteria like subscription status
            return True
    return False
