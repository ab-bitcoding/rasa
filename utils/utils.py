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
    """
    Fetches all user data from the API.

    This function sends a GET request to the specified API endpoint to retrieve user data.
    It checks if the API base URL is set and returns the data in JSON format if the request
    is successful. If the request fails, it returns an empty dictionary.

    Returns:
        Dict[Text, Any]: The user data fetched from the API in JSON format. If the request fails,
                         returns an empty dictionary.

    Raises:
        ValueError: If the API_BASE_URL environment variable is not set.
    """

    if not API_BASE_URL:
        raise ValueError("API_BASE_URL environment variable is not set.")

    url = f"{API_BASE_URL}/all_users"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {}


def fetch_user_data(phone_number: str) -> Dict[str, Any]:
    """
    Fetches user data from the API for a given phone number.

    Args:
        phone_number (str): User's phone number.

    Returns:
        dict: User data in JSON format if successful, otherwise an empty dictionary.

    Raises:
        ValueError: If API_BASE_URL is not set.
        requests.exceptions.RequestException: For request failures.
    """

    if not API_BASE_URL:
        raise ValueError("API_BASE_URL environment variable is not set.")


    url = f"{API_BASE_URL}/user/{phone_number}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return {}


def update_user_details(phone_number: str, payload: dict) -> dict:
    """
    Updates the user's details in the system via an API call.

    This function sends a PUT request to the API endpoint to update the details of
    a user identified by the given phone number. It handles potential HTTP errors
    and other exceptions, returning the response data from the API call if successful.
    If the request fails or an error occurs, it returns an empty dictionary.

    Args:
        phone_number (str): The phone number of the user whose details are to be updated.
        payload (dict): The dictionary containing the data to update, formatted as JSON.

    Returns:
        dict: The response data from the API call. If the request fails or an error occurs,
              returns an empty dictionary.

    Raises:
        ValueError: If the API_BASE_URL environment variable is not set.
        requests.exceptions.HTTPError: If an HTTP error occurs during the request.
        Exception: For other general exceptions during the request.
    """

    if not API_BASE_URL:
        raise ValueError("API_BASE_URL environment variable is not set.")

    url = f"{API_BASE_URL}/user/{phone_number}"

    try:
        response = requests.put(url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")
    return {}

