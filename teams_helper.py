import requests
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def generate_auth_token(creds):
    # Generates the auth token
    url = os.environ.get('auth_token_url')

    payload = {
        "grant_type": "client_credentials",
        "client_id": creds["client_id"],
        "client_secret": creds["client_secret"],
        "scope": creds["scope"]
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code == 200:
        return "Bearer " + response.json().get("access_token")


def get_user_email(conversation_id, user_id, creds):
    """
    Returns the user email from the conversation_id and user_id
    """
    try:
        url = creds["user_details_url"]
        user_details_url = f"{url}/conversations/{conversation_id}/members/{user_id}"
        headers = {
            "Authorization": generate_auth_token(creds),
            "Content-Type": "application/json"
        }
        response =  requests.request("GET", user_details_url, headers=headers)
        if response.status_code == 200:
            return response.json().get("email")
        logger.error(f"Couldn't retrieve the user email due to status: {response.status_code} and\n\n{response.text}")
    except Exception as ex:
        logger.error(f"Raised an exception while fetching user email: {ex}")
