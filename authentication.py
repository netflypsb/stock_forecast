import requests
import streamlit as st

def fetch_subscribers(access_token=None):
    """
    Fetch all active subscribers with their plan details.
    This function checks the API response carefully and handles any missing or unexpected data.
    """
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

def is_subscriber_authorized(email, plan_name, subscribers):
    """
    Check if the provided email subscribes to the specified plan.
    Includes checks to safely access 'email' and 'plan' keys.
    """
    for subscriber in subscribers:
        # Ensure both 'email' and 'plan' keys exist in each subscriber dictionary
        if 'email' in subscriber and 'plan' in subscriber:
            if subscriber['email'] == email and subscriber['plan'] == plan_name:
                return True
        else:
            # Optionally log or handle entries with missing data
            st.warning(f"Missing required data for a subscriber entry: {subscriber}")
    return False
