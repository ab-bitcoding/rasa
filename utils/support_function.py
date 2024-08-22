def get_main_menu_buttons():
    """
    Returns a list of buttons for the main menu.

    Each button is represented by a dictionary with a title and payload.
    
    Returns:
        list: A list of dictionaries, each representing a button with a title and payload.
    """
    return [
        {"title": "Renew Policy", "payload": '/renew_policy'},
        {"title": "Claims Related", "payload": '/claims_related'},
        {"title": "Download Policy Copy", "payload": '/download_policy'},
        {"title": "Emergency Support", "payload": '/emergency_support'},
        {"title": "Nearby Workshop", "payload": '/near_by_workshop'},
        {"title": "New Policy", "payload": '/new_policy'},
        {"title": "Health Policy", "payload": '/health_policy'},
        {"title": "User Details", "payload": '/user_details'}
    ]

def get_main_menu_message():
    """
    Constructs a message offering help with insurance-related support and prompts the user to click on the Main Menu.

    Returns:
        str: A formatted message encouraging the user to seek help and navigate to the main menu.
    """
    message = (
        "Need help with renewal, claims or any other insurance-related support. \n \n"
        "Click on *Main Menu*"
    )
    return message


def get_update_and_confirm_data_buttons():
    """
    Returns a list of buttons for updating and confirming user data.

    Each button is represented by a dictionary with a title and payload.
    
    Returns:
        list: A list of dictionaries, each representing a button with a title and payload.
    """
    return [
        {"title": "Update", "payload": '/update_user_details'},
        {"title": "Confirm", "payload": '/confirm_user_details'}
    ]


def get_user_info_message(username, email, age, phone_number, income):
    """
    Constructs a message containing user details.

    Args:
        username (str): The username of the user.
        email (str): The email address of the user.
        age (str): The age of the user.
        phone_number (str): The phone number of the user.
        income (str): The income of the user.

    Returns:
        str: A formatted message with the user details.
    """
    message = (
        "Having trouble updating the data? 🔄 Use the *Update* and *Confirm* button. Let us know if you need help. 🤝 \n \n"
        "🔍 Here's the information About you:\n"
        f"👤 *Username:* {username} \n"
        f"📧 *Email:* {email} \n"
        f"🎂 *Age:* {age} \n"
        f"📞 *Phone Number:* {phone_number} \n"
        f"💼 *Income:* {income} \n"
    )
    return message

def extract_user_details(user_data):
    """
    Extracts user details such as username, email, age, and income from the provided user data.

    Args:
        user_data (dict): A dictionary containing user information.

    Returns:
        tuple: A tuple containing username, email, age, and income.
               If a detail is missing, its value in the tuple will be None.
    """
    username = user_data.get('username')
    email = user_data.get('email')
    age = user_data.get('age')
    income = user_data.get('income')
    
    return username, email, age, income
