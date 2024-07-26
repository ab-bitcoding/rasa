import os
import requests
from dotenv import load_dotenv
from typing import Dict

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
    
    url = f"{API_BASE_URL}/user/"

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to submit form: {str(e)}")
