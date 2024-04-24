import requests
import streamlit as st

def fetch_subscribers(access_token=None):
    """Fetch all active subscribers with their plan details."""
    if access_token is None:
        access_token = st.secrets["eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI5MTI5ZDIwMC1kYTdkLTRjY2MtOWQzZC01ODA0MTU0ZTgyMjYiLCJqdGkiOiI3NDBjMGZlNmYyOWZiM2RiNTczNmFiZTAzYThlMmQ2ZDcxY2E3OWM0NjY2NzNlMTk3Mzk5NmQxNzg3NDcwZjI5ZDczNzY4MzVjNmE3NzVkNSIsImlhdCI6MTcxMzkzNzYwNywibmJmIjoxNzEzOTM3NjA3LCJleHAiOjE3Mjk3NDg4MDcsInN1YiI6IjUwNDQ4NjAiLCJzY29wZXMiOltdfQ.nX7lyIfaBgZhyvyRGRegqTuYC0dzJqpJj_2t0ItNMZFkz1sUvvdUoYJkV03gHg78q0g7R93mQjZkSnOrDAH6Zx1jtKlecagO9BQDSMa9fywkd_B6Xvp6DunxhAkEv5wfRqiMAYop8dlUFjr2QkwSrXi67YZFBC0GF5a4HCNPeLcxGIeL32yJOML_axRC9JBpn7vVHfBJjC0h1OiW9xuWb4-dmHWA0Eern6A1ov5zZ2iyCuT0LXxHpGmrl3TIqVcPd3VShJG2e7cAIYt3ZIbxOGOzhP6hDOcPYqg_yBLrV5t76V3_qfoUs5Jg5_64M1Y1liBTUBlOTjV4C143t-45RYkIWuL5mVdYqCTZEZ-fVsYN7mUonGLwfBrMqmHSw7ltk3XH8L7z3X_iYV7UXA47MI29_vUf1l_tKuKuBy5d_t1ZD5rreFLPajA9OsAkHxsCj3riu9s7an2n4Nu4r9nsmY4xae3Ivw8JTrR0HeUf42trS9fTUyFDZbdKEJHfXijN2g4Z8eRILGjUWubr3HpKFhOMrsXw8d_xapP3TRCslSZtCv8ejKUahKsQs1u3VOCbp2iv-1Qcz3n_g-WIenxveRk6iN762Ac9QL74-EBkxWgXjuUramGdeK5K5tSCiV-KXB31E05IIqy29OFcHZg4-nyykL94jUvhlegFhHIaCZY"]
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
