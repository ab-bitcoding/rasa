import os
import requests
from dotenv import load_dotenv
from typing import Any, Dict, List, Text

# Load environment variables from the .env file
load_dotenv()

# Retrieve the API base URL from environment variables
API_BASE_URL = os.getenv("API_BASE_URL")

def create_user(payload: Dict[str, any]) -> Dict[str, any]:
    """
    Submits form data to the configured API endpoint.

    Args:
        payload (Dict[str, any]): A dictionary containing the form data to be sent to the API.

    Returns:
        Dict[str, any]: The JSON response from the API.

    Raises:
        Exception: If the API request fails or an unexpected error occurs.
    """
    if not API_BASE_URL:
        raise ValueError("API_BASE_URL environment variable is not set.")
    
    url = f"{API_BASE_URL}/user"

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to submit form: {str(e)}")


def fetch_all_user_data() -> Dict[Text, Any]:

    if not API_BASE_URL:
        raise ValueError("API_BASE_URL environment variable is not set.")
    
    url = f"{API_BASE_URL}/all_users"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return []

def fetch_user_data(phone_number: str) -> Dict[str, Any]:
    url = f"http://127.0.0.1:8000/v1/user/{phone_number}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching data: {response.status_code}")
            return {}
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return {}


def update_user_details(phone_number: str, payload: dict) -> dict:
    """
    Updates the user's details in the system.

    Args:
        phone_number (str): The phone number of the user.
        payload (dict): The dictionary containing the data to update.

    Returns:
        dict: The response data from the API call.
    """
    url = f"http://127.0.0.1:8000/v1/user/{phone_number}"

    try:
        response = requests.put(url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")
    return {}

