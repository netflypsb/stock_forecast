import requests
import streamlit as st

def fetch_subscribers(access_token=None):
    """
    Fetch all active subscribers that are subscribed to membership ID 187451.
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
    Check if the provided email subscribes to the specific membership level with ID 187451.
    """
    for subscriber in subscribers:
        if ('payer_email' in subscriber and 'membership_level_id' in subscriber and
            subscriber['payer_email'] == email and subscriber['membership_level_id'] == 187452):
            return True
    return False
