import requests
import streamlit as st

def fetch_subscribers(access_token=None):
    """Fetch all active subscribers with their plan details."""
    if access_token is None:
        access_token = st.secrets["bmac_api_key"]
    url = "https://developers.buymeacoffee.com/api/v1/subscriptions"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)

    # Check if the response was successful
    if response.status_code == 200:
        json_response = response.json()
        # Check if 'data' key is present in the response
        if 'data' in json_response:
            return json_response['data']
        else:
            # Log error or handle cases where 'data' is not present
            st.error("Received unexpected data structure from BMAC API.")
            return []
    else:
        # Handle response errors
        st.error(f"Failed to fetch subscribers: {response.status_code} - {response.text}")
        return []
