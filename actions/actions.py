import os
import re
import requests
from dotenv import load_dotenv
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction, AllSlotsReset
from rasa_sdk.types import DomainDict

from utils.utils import (
    create_user,
    fetch_user_data,
    fetch_all_user_data,
    update_user_details
)
from utils.support_function import (
    get_main_menu_buttons,
    get_update_and_confirm_data_buttons,
    get_user_info_message,
    get_main_menu_message,
    extract_user_details
)
load_dotenv()


class ActionGreetUser(Action):
    def name(self) -> Text:
        """
        Returns the name of the action.
        
        This action is responsible for greeting the user by retrieving their 
        phone number from the metadata, fetching user data, and then sending 
        a personalized greeting message with language selection options.
        
        Returns:
            str: The name of the action "action_greet_user".
        """
        return "action_greet_user"

    def run(self, 
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """
        Executes the action when called by Rasa.

        This method retrieves the user's phone number from the message metadata,
        fetches the corresponding user data, and sends a personalized greeting 
        message. If user data is found, the message includes the user's name; 
        otherwise, a generic greeting is sent. The user is then prompted to select 
        their preferred language.

        Args:
            dispatcher (CollectingDispatcher): The dispatcher to send messages back to the user.
            tracker (Tracker): The tracker that keeps track of the conversation state.
            domain (Dict[Text, Any]): The domain dictionary containing the bot's intents, actions, etc.

        Returns:
            List[Dict[Text, Any]]: A list of events that Rasa should process after the action is run. 
                                   This includes setting the "phone_number" slot, and if user data is 
                                   found, the "name" slot as well.
        """
        
        # Retrieve the mobile number from metadata
        metadata = tracker.latest_message.get('metadata', {})
        user_phone_number = metadata.get("sender")
        print(f"greet user_phone_number: {user_phone_number}")

        if user_phone_number:
            user_data = fetch_user_data(user_phone_number)
            if user_data:
                name  = user_data.get('username')

                message = (
                    f"Hi *{name}*,\n \n"
                    "I am Liberty Buddy, Your WhatsApp Insurance Assistant.\n \n"
                    "Let's get started with your renewal, claims, or any other insurance-related support.\n \n"
                    "Please select your language."
                )
                buttons = [
                    {"title": "English", "payload": '/select_language{"language":"english"}'},
                    {"title": "Hindi", "payload": '/select_language{"language":"hindi"}'}
                ]

                dispatcher.utter_message(text=message, buttons=buttons)
                return [
                    SlotSet("phone_number", user_phone_number),
                    SlotSet("name", name)
                ]

            else:
                message = (
                    "Hi,\n  \n"
                    "I'm Liberty Buddy, Your WhatsApp Insurance Assistant.\n  \n"
                    "I help you for Renewals, Claims, and Any other Insurance Support.\n  \n"
                    "So, Let's get started.\n \n"
                    "Please select your preferred language."
                )
                buttons = [
                    {"title": "English", "payload": '/select_language{"language":"english"}'},
                    {"title": "Hindi", "payload": '/select_language{"language":"hindi"}'}
                ]
                dispatcher.utter_message(text=message, buttons=buttons)
                return [SlotSet("phone_number", user_phone_number)]


class ActionSelectLanguage(Action):
    """
    A Rasa custom action that handles language selection by the user.

    This action checks the language selected by the user, normalizes the value, and responds
    with the appropriate main menu message and buttons in the selected language.
    """

    def name(self) -> Text:
        """
        Returns the name of the action.

        This method is used by Rasa to identify the action by name.

        Returns:
            str: The name of the action, "action_select_language".
        """
        return "action_select_language"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """
        Executes the action to handle the user's language selection.

        This method extracts the language value from the user's slot, normalizes it by capitalizing 
        the first letter, and responds with a main menu message and buttons if the language is English. 
        If no language is provided, it defaults to "Unknown".

        Args:
            dispatcher (CollectingDispatcher): The dispatcher used to send messages back to the user.
            tracker (Tracker): The tracker that keeps track of the conversation state.
            domain (Dict[Text, Any]): The domain dictionary containing the bot's intents, actions, etc.

        Returns:
            List[Dict[Text, Any]]: A list of events that Rasa should process after the action is run. 
                                   This includes setting the "language" slot to the normalized language.
        """

        # Extract the language slot value
        language = tracker.get_slot("language")

        # Check if the language slot is set correctly
        print("Extracted slot value:", language)

        # Normalize the language value
        if language:
            normalized_language = language.capitalize()  # Capitalize the first letter
        else:
            normalized_language = "Unknown"  # Handle cases where no language is provided

        # Respond based on the normalized language
        if normalized_language == "English":

            message = get_main_menu_message()
            buttons = get_main_menu_buttons()

            dispatcher.utter_message(text=message, buttons=buttons)
            return [SlotSet("language", normalized_language)]


class ActionEmergencySupport(Action):
    """
    A Rasa custom action that provides emergency support information to the user.

    This action sends a message to the user with instructions on how to connect with the nearest workshop
    by entering their pincode and sharing their current location. It also provides emergency contact
    numbers for immediate assistance.
    """

    def name(self) -> Text:
        """
        Returns the name of the action.

        This method is used by Rasa to identify the action by name.

        Returns:
            str: The name of the action, "action_emergency_support".
        """
        return "action_emergency_support"
    
    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """
        Executes the action to provide emergency support information.

        This method sends a message to the user with details on how to find the nearest workshop 
        by entering their pincode and sharing their location. It also includes emergency contact 
        numbers for additional support.

        Args:
            dispatcher (CollectingDispatcher): The dispatcher used to send messages back to the user.
            tracker (Tracker): The tracker that keeps track of the conversation state.
            domain (Dict[Text, Any]): The domain dictionary containing the bot's intents, actions, etc.

        Returns:
            List[Dict[Text, Any]]: An empty list as no slots or other events are set by this action.
        """
        
        message = (
            "In case you need repair service, enter the pincode and share your current location to connect with the nearest workshop. \n \n"
            "If you require any assistance, \n \n"
            "Call - *1800XXXXXXXXX* \n"
            "Missed call and get a callback: \n"
            "9876543211"
        )
        dispatcher.utter_message(text=message)
        return []


class ValidateEmergencySupportPincodeForm(FormValidationAction):
    """
    A Rasa custom action that validates the pincode and location coordinates 
    (latitude and longitude) provided by the user for emergency support.
    
    This form validation action ensures that either a valid pincode or valid 
    latitude and longitude coordinates are provided before proceeding.
    """

    def name(self) -> Text:
        """
        Returns the name of the form validation action.

        This method is used by Rasa to identify the action by name.

        Returns:
            str: The name of the action, "validate_emergency_support_pincode_form".
        """
        return "validate_emergency_support_pincode_form"

    def validate_pincode(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        """
        Validates the pincode or location coordinates (latitude and longitude) provided by the user.

        This method first checks if both latitude and longitude are provided and within the valid range.
        If they are, it sets the corresponding slots. If not, it checks the pincode. If neither is valid 
        after three failed attempts, fallback values are returned.

        Args:
            slot_value (Any): The value of the slot being validated.
            dispatcher (CollectingDispatcher): The dispatcher used to send messages back to the user.
            tracker (Tracker): The tracker that keeps track of the conversation state.
            domain (Dict[Text, Any]): The domain dictionary containing the bot's intents, actions, etc.

        Returns:
            List[Dict[Text, Any]]: A list of slot dictionaries to set or reset slots based on validation.
        """

        emergency_pincode = tracker.get_slot('pincode')
        latitude = tracker.get_slot('latitude')
        longitude = tracker.get_slot('longitude')

        print(f"emergency_pincode: {emergency_pincode}")
        print(f"latitude: {latitude}")
        print(f"longitude: {longitude}")

        failed_attempts = tracker.get_slot('failed_attempts') or 0

        if None not in (latitude, longitude):
            if -180 <= float(latitude) <= 180 and -180 <= float(longitude) <= 180:
                print("Inside match if Condition")
                set_latitude_and_longitude_slot = {"latitude": latitude, "longitude": longitude}
                print(f"set_latitude_and_longitude_slot: {set_latitude_and_longitude_slot}")
                return set_latitude_and_longitude_slot
            else:
                failed_attempts += 1
                if failed_attempts == 3:
                    get_update_latitude_longitude = {"latitude": "fallback", "longitude": "fallback", "failed_attempts": None}
                    print(f"get_update_latitude_longitude: {get_update_latitude_longitude}")
                    return get_update_latitude_longitude
                else:
                    dispatcher.utter_message(text="The provided location coordinates are invalid.")
                    attempts_value = {"failed_attempts": failed_attempts, "latitude": None, "longitude": None, "pincode": None}
                    print(f"failed_attempts_value: {attempts_value}")
                    return attempts_value
        else:
            if emergency_pincode and len(emergency_pincode) == 6 and emergency_pincode.isdigit():
                print("Inside Validate pincode if Condition")
                set_pincode_slot = {"pincode": emergency_pincode}
                print(f"set_pincode_slot: {set_pincode_slot}")
                return set_pincode_slot
            else:
                failed_attempts = failed_attempts + 1
                if failed_attempts == 3:
                    get_pincode = {"pincode": "fallback", "failed_attempts": None}
                    print(f"get_pincode: {get_pincode}")
                    return get_pincode
                else:
                    dispatcher.utter_message(text="Looks like the pincode is invalid. Please enter a valid 6-digit pincode or share your current location.")
                    attempts_value = {"failed_attempts": failed_attempts, "pincode": None}
                    print(f"failed_attempts_value: {attempts_value}")
                    return attempts_value


class ActionSubmitEmergencyPincodeForm(Action):
    """
    A Rasa custom action that handles the submission of the emergency support 
    pincode form. This action checks the user's provided pincode or location 
    coordinates (latitude and longitude) and provides appropriate responses.

    If the pincode or coordinates are marked as "fallback" due to validation failure,
    the user is redirected to the main menu. Otherwise, it provides details of nearby 
    garages along with a link to view the garages on a map.
    """

    def name(self) -> Text:
        """
        Returns the name of the custom action.

        This method is used by Rasa to identify the action by name.

        Returns:
            str: The name of the action, "action_submit_emergency_support_pincode_form".
        """
        return "action_submit_emergency_support_pincode_form"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: "DomainDict") -> List[Dict[Text, Any]]:
        """
        Executes the action to handle the submission of the emergency support pincode form.

        This method checks the pincode or location coordinates provided by the user.
        If either of these is invalid (indicated by "fallback"), the user is redirected to the main menu.
        If valid, it provides details of nearby garages and a link to view them on a map.

        Args:
            dispatcher (CollectingDispatcher): The dispatcher used to send messages back to the user.
            tracker (Tracker): The tracker that keeps track of the conversation state.
            domain (DomainDict): The domain dictionary containing the bot's intents, actions, etc.

        Returns:
            List[Dict[Text, Any]]: A list of SlotSet events to reset the pincode, latitude, longitude, and failed_attempts slots.
        """

        emergency_pincode = tracker.get_slot("pincode")
        latitude = tracker.get_slot("latitude")
        longitude = tracker.get_slot("longitude")
        print("emergency_pincode::::", emergency_pincode)

        if emergency_pincode == "fallback" or (latitude, longitude) == ("fallback", "fallback"):
            
            message = get_main_menu_message()
            buttons = get_main_menu_buttons()

            dispatcher.utter_message(text=message, buttons=buttons)
            return [
                SlotSet("pincode", None),
                SlotSet("latitude", None),
                SlotSet("longitude", None),
                SlotSet("failed_attempts", None)
            ]
        else:
            message = (
                "Great! We found 1 Garage near you. Given below are the details of workshops: \n \n"
                "*Superon* \n"
                "Tele No: 9876543211 \n \n"
                "*Safdarjang* \n"
                "Tele No: 8765432123 \n \n"
                "Click the link below to view garages on the map: \n"
                "https://dxa2.jcowk/oxwo=jcwojcown \n \n"
                "If you require any assistance, \n \n"
                "Call - *1800XXXXXXXXX* \n"
                "Missed call and get a callback: \n"
                "9876543211"
            )
            buttons = get_main_menu_buttons()

            dispatcher.utter_message(text=message, buttons=buttons)
            return [
                SlotSet("pincode", None),
                SlotSet("latitude", None),
                SlotSet("longitude", None),
                SlotSet("failed_attempts", None)
            ]


class ActionNearByWorkshop(Action):
    """
    A Rasa custom action that prompts the user to provide their pincode or 
    current location to assist them in finding nearby workshops.

    This action sends a message requesting the user to enter their pincode 
    or share their location.
    """

    def name(self) -> Text:
        """
        Returns the name of the custom action.

        This method is used by Rasa to identify the action by name.

        Returns:
            str: The name of the action, "action_near_by_workshop".
        """
        return "action_near_by_workshop"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """
        Executes the action to prompt the user for their pincode or current location.

        This method sends a message to the user, asking them to enter their pincode 
        or share their current location so they can be assisted in finding a nearby workshop.

        Args:
            dispatcher (CollectingDispatcher): The dispatcher used to send messages back to the user.
            tracker (Tracker): The tracker that keeps track of the conversation state.
            domain (Dict[Text, Any]): The domain dictionary containing the bot's intents, actions, etc.

        Returns:
            List[Dict[Text, Any]]: An empty list as no slots are set in this action.
        """
        message = (
            "🙂 We are happy to assist you.\n \n"
            "Please enter the Pincode or share your current location."
        )

        dispatcher.utter_message(text=message)
        return []


class ValidateNearByWorkshopPincodeForm(FormValidationAction):
    """
    A Rasa custom action for validating the pincode or location data in a form submission.
    
    This action validates the pincode or the location coordinates (latitude and longitude) 
    provided by the user. It checks the validity of the coordinates and the pincode, 
    handling cases where invalid data is provided or where multiple failed attempts 
    occur. If the data is valid, it updates the corresponding slot; otherwise, it prompts 
    the user to provide correct information.
    """

    def name(self) -> Text:
        """
        Returns the name of the custom validation action.

        This method is used by Rasa to identify the action by name.

        Returns:
            str: The name of the action, "validate_near_by_workshop_pincode_form".
        """
        return "validate_near_by_workshop_pincode_form"
    
    def validate_pincode(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """
        Validates the pincode or location coordinates provided by the user.

        This method checks whether the pincode is a valid 6-digit number or whether 
        the latitude and longitude are within valid ranges. It handles cases of 
        invalid data and tracks failed attempts to validate the data. After validation, 
        it returns the appropriate slot values or prompts the user to provide correct 
        information if needed.

        Args:
            slot_value (Any): The value of the pincode slot to be validated.
            dispatcher (CollectingDispatcher): The dispatcher used to send messages back to the user.
            tracker (Tracker): The tracker that keeps track of the conversation state.
            domain (Dict[Text, Any]): The domain dictionary containing the bot's intents, actions, etc.

        Returns:
            List[Dict[Text, Any]]: A list of slot updates based on the validation results.
        """
        pincode = tracker.get_slot('pincode')
        latitude = tracker.get_slot('latitude')
        longitude = tracker.get_slot('longitude')
        failed_attempts = tracker.get_slot('failed_attempts') or 0

        if None not in (latitude, longitude):
            if -180 <= float(latitude) <= 180 and -180 <= float(longitude) <= 180:
                print("Inside match if Condition")
                set_latitude_and_longitude_slot = {"latitude": latitude, "longitude": longitude}
                print(f"set_latitude_and_longitude_slot: {set_latitude_and_longitude_slot}")
                return set_latitude_and_longitude_slot
            else:
                failed_attempts = failed_attempts + 1
                if failed_attempts == 3:
                    get_update_latitude_longitude = {"latitude": "fallback", "longitude": "fallback", "failed_attempts": None}
                    print(f"get_update_latitude_longitude: {get_update_latitude_longitude}")
                    return get_update_latitude_longitude
                else:
                    dispatcher.utter_message(text="The provided location coordinates are invalid.")
                    attemps_value = {"failed_attempts": failed_attempts, "latitude": None, "longitude": None, "pincode": None}
                    print(f"failed_attemps_value: {attemps_value}")
                    return attemps_value
        else:
            if pincode and len(pincode) == 6 and pincode.isdigit():
                print("Inside Validate pincode if Condition")
                set_pincode_slot = {"pincode": pincode}
                print(f"set_pincode_slot: {set_pincode_slot}")
                return set_pincode_slot
            else:
                failed_attempts = failed_attempts + 1
                if failed_attempts == 3:
                    get_pincode = {"pincode": "fallback", "failed_attempts": None}
                    print(f"get_pincode: {get_pincode}")
                    return get_pincode
                else:
                    dispatcher.utter_message(text="Looks like the pincode is invalid. Please enter a valid 6-digit pincode or share your current location.")
                    attemps_value = {"failed_attempts": failed_attempts, "pincode": None}
                    print(f"failed_attemps_value: {attemps_value}")
                    return attemps_value


class ActionSubmitNearByWorkshopPincodeForm(Action):
    """
    A Rasa custom action for handling the submission of the Nearby Workshop Pincode form.

    This action processes the form submission by checking the values of the pincode, latitude, and longitude
    slots. It either provides information about nearby workshops based on the provided pincode or location 
    or redirects the user to the main menu if the provided data is invalid or marked as "fallback".
    """

    def name(self) -> Text:
        """
        Returns the name of the custom action.

        This method is used by Rasa to identify the action by name.

        Returns:
            str: The name of the action, "action_submit_near_by_workshop_pincode_form".
        """
        return "action_submit_near_by_workshop_pincode_form"
    
    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> List[Dict[Text, Any]]:
        """
        Executes the action to handle the submission of the Nearby Workshop Pincode form.

        This method checks if the pincode or location data is valid. If the data is valid, it sends a message 
        with details of nearby workshops. If the data is invalid or marked as "fallback", it redirects the user 
        to the main menu with appropriate buttons. It also resets relevant slots.

        Args:
            dispatcher (CollectingDispatcher): The dispatcher used to send messages back to the user.
            tracker (Tracker): The tracker that keeps track of the conversation state.
            domain (DomainDict): The domain dictionary containing the bot's intents, actions, etc.

        Returns:
            List[Dict[Text, Any]]: A list of slot updates and actions based on the validity of the provided data.
        """
        pincode = tracker.get_slot('pincode')
        latitude = tracker.get_slot('latitude')
        longitude = tracker.get_slot('longitude')

        if pincode == "fallback" or (latitude, longitude) == ("fallback", "fallback"):
            message = get_main_menu_message()
            buttons = get_main_menu_buttons()

            dispatcher.utter_message(text=message, buttons=buttons)
            return [
                SlotSet("pincode", None),
                SlotSet("latitude", None),
                SlotSet("longitude", None),
                SlotSet("failed_attempts", None)
            ]
        else:
            message = (
                "Great! We found 1 Garage near you. Given below are the details of workshops: \n \n"
                "*Superon* \n"
                "Tele No: 9876543211 \n \n"
                "*Safdarjang* \n"
                "Tele No: 8765432123 \n \n"
                "Click the link below to view garages on the map: \n"
                "https://dxa2.jcowk/oxwo=jcwojcown \n \n"
                "If you require any assistance, \n \n"
                "Call - *1800XXXXXXXXX* \n"
                "Missed call and get a callback: \n"
                "9876543211"
            )
            buttons = get_main_menu_buttons()

            dispatcher.utter_message(text=message, buttons=buttons)
            return [
                SlotSet("pincode", None),
                SlotSet("latitude", None),
                SlotSet("longitude", None),
                SlotSet("failed_attempts", None)
            ]


class ActionRenewPolicy(Action):
    """
    A Rasa custom action for handling policy renewal requests.

    This action sends a message to the user indicating that they have requested to renew their policy. 
    The message typically prompts the user to take further actions related to policy renewal.
    """

    def name(self) -> Text:
        """
        Returns the name of the custom action.

        This method is used by Rasa to identify the action by name.

        Returns:
            str: The name of the action, "action_renew_policy".
        """
        return "action_renew_policy"
    
    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """
        Executes the action to handle policy renewal requests.

        This method sends a message to the user indicating that the policy renewal process has been initiated. 
        It does not perform any additional actions beyond sending the message.

        Args:
            dispatcher (CollectingDispatcher): The dispatcher used to send messages back to the user.
            tracker (Tracker): The tracker that keeps track of the conversation state.
            domain (Dict[Text, Any]): The domain dictionary containing the bot's intents, actions, etc.

        Returns:
            List[Dict[Text, Any]]: An empty list, as no slot updates or additional actions are required.
        """
        message = (
            """
            Renew Policy
            """
        )
        dispatcher.utter_message(text=message)
        return []


class ActionHealthPolicy(Action):
    """
    A Rasa custom action for handling health policy-related requests.

    This action is triggered when a user navigates to the health policy section.
    It prompts the user to fill out a form and provides instructions for the next steps.
    """

    def name(self) -> Text:
        """
        Returns the name of the custom action.

        This method is used by Rasa to identify the action by its name.

        Returns:
            str: The name of the action, "action_health_policy".
        """
        return "action_health_policy"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """
        Executes the action for handling health policy requests.

        This method sends a message to the user indicating that they are now in the health policy section.
        It also provides instructions for the next steps, such as filling out a form and entering their name.

        Args:
            dispatcher (CollectingDispatcher): The dispatcher used to send messages back to the user.
            tracker (Tracker): The tracker that keeps track of the conversation state.
            domain (Dict[Text, Any]): The domain dictionary containing the bot's intents, actions, etc.

        Returns:
            List[Dict[Text, Any]]: An empty list, as no slot updates or additional actions are required.
        """
        message = (
            "You are now in the Health Policy section. \n \n"
            "Please fill out the form for the Health Policy. \n \n"
            "We need some details to proceed with your request. Thank you! \n \n"
            "Please enter your name"
        )
        dispatcher.utter_message(text=message)
        return []


class ValidateHealthPolicyForm(FormValidationAction):
    """
    A Rasa custom action for validating the Health Policy form input.

    This action validates user inputs for the Health Policy form, including name, email, age, phone number, and income.
    Each validation method checks the format and validity of the input and provides appropriate feedback to the user.
    """

    def name(self) -> Text:
        """
        Returns the name of the form validation action.

        This method is used by Rasa to identify the action by its name.

        Returns:
            str: The name of the action, "validate_health_policy_form".
        """
        return "validate_health_policy_form"

    def validate_name(
                      self,
                      slot_value: Any,
                      dispatcher: CollectingDispatcher,
                      tracker: Tracker,
                      domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """
        Validates the user's name input.

        This method checks if the name provided is a valid alphabetical string with more than one character.
        If valid, it prompts the user to provide their email. Otherwise, it asks the user to enter a valid name.

        Args:
            slot_value (Any): The value of the slot to be validated.
            dispatcher (CollectingDispatcher): The dispatcher used to send messages back to the user.
            tracker (Tracker): The tracker that keeps track of the conversation state.
            domain (Dict[Text, Any]): The domain dictionary containing the bot's intents, actions, etc.

        Returns:
            List[Dict[Text, Any]]: A list with the updated slot values. The "name" slot is updated with the validated name or `None` if invalid.
        """
        name = tracker.get_slot('name').lower()
        print(f"This is name: {name}")
        if name.replace(" ", "").isalpha() and len(name) > 1:
            dispatcher.utter_message(text="Thanks! Now, could you please provide your email?")
            return {"name": name}
        else:
            dispatcher.utter_message(text="Please enter a valid name.")
            return {"name": None}

    def validate_email(
                       self,
                       slot_value: Any,
                       dispatcher: CollectingDispatcher,
                       tracker: Tracker,
                       domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """
        Validates the user's email input.

        This method checks if the email provided contains "@" and "." and has a length greater than 7 characters.
        If valid, it prompts the user to provide their age. Otherwise, it asks the user to enter a valid email address.

        Args:
            slot_value (Any): The value of the slot to be validated.
            dispatcher (CollectingDispatcher): The dispatcher used to send messages back to the user.
            tracker (Tracker): The tracker that keeps track of the conversation state.
            domain (Dict[Text, Any]): The domain dictionary containing the bot's intents, actions, etc.

        Returns:
            List[Dict[Text, Any]]: A list with the updated slot values. The "email" slot is updated with the validated email or `None` if invalid.
        """
        get_email = tracker.get_slot('email').strip().lower()
        email = re.sub(r'\s+', '', get_email)
        print(f"This is email: {email}")
        if "@" in email and "." in email and len(email) > 7:
            dispatcher.utter_message(text="Thanks! Now, could you please provide your age?")
            return {"email": email}
        else:
            dispatcher.utter_message(text="Please enter a valid email address.")
            return {"email": None}

    def validate_age(
                    self,
                    slot_value: Any,
                    dispatcher: CollectingDispatcher,
                    tracker: Tracker,
                    domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """
        Validates the user's age input.

        This method checks if the age provided is a positive integer between 1 and 120.
        If valid, it prompts the user to provide their phone number. Otherwise, it asks the user to enter a valid age.

        Args:
            slot_value (Any): The value of the slot to be validated.
            dispatcher (CollectingDispatcher): The dispatcher used to send messages back to the user.
            tracker (Tracker): The tracker that keeps track of the conversation state.
            domain (Dict[Text, Any]): The domain dictionary containing the bot's intents, actions, etc.

        Returns:
            List[Dict[Text, Any]]: A list with the updated slot values. The "age" slot is updated with the validated age or `None` if invalid.
        """
        age = tracker.get_slot('age')
        print(f"This is age: {age}")
        if age and 0 < int(age) <= 120:
            dispatcher.utter_message(text="Thanks! Now, could you please provide your Phone Number?") 
            return {"age": age}
        else:
            dispatcher.utter_message(text="Please enter a valid age")
            return {"age": None}

    def validate_phone_number(
                    self,
                    slot_value: Any,
                    dispatcher: CollectingDispatcher,
                    tracker: Tracker,
                    domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """
        Validates the user's phone number input.

        This method checks if the phone number provided contains only digits and is up to 15 characters long.
        If valid, it prompts the user to provide their income. Otherwise, it asks the user to enter a valid phone number.

        Args:
            slot_value (Any): The value of the slot to be validated.
            dispatcher (CollectingDispatcher): The dispatcher used to send messages back to the user.
            tracker (Tracker): The tracker that keeps track of the conversation state.
            domain (Dict[Text, Any]): The domain dictionary containing the bot's intents, actions, etc.

        Returns:
            List[Dict[Text, Any]]: A list with the updated slot values. The "phone_number" slot is updated with the validated phone number or `None` if invalid.
        """
        phone_number = tracker.get_slot('phone_number')
        print(f"This is Phone Number: {phone_number}")
        if phone_number.isdigit() and len(phone_number) <= 15:
            dispatcher.utter_message(text="Thanks! Now, could you please provide your Income?") 
            return {"phone_number": phone_number}
        else:
            dispatcher.utter_message(text="Please enter a valid phone number")
            return {"phone_number": None}

    def validate_income(
                    self,
                    slot_value: Any,
                    dispatcher: CollectingDispatcher,
                    tracker: Tracker,
                    domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """
        Validates the user's income input.

        This method checks if the income provided is a valid positive number.
        If valid, it sets the income slot. Otherwise, it asks the user to enter a valid numeric income.

        Args:
            slot_value (Any): The value of the slot to be validated.
            dispatcher (CollectingDispatcher): The dispatcher used to send messages back to the user.
            tracker (Tracker): The tracker that keeps track of the conversation state.
            domain (Dict[Text, Any]): The domain dictionary containing the bot's intents, actions, etc.

        Returns:
            List[Dict[Text, Any]]: A list with the updated slot values. The "income" slot is updated with the validated income or `None` if invalid.
        """
        income = tracker.get_slot('income')
        print(f"This is Income: {income}")
        try:
            income_value = float(income)
            if income_value > 0:
                return {"income": income}
            else: 
                dispatcher.utter_message(text="Please enter a valid income")
                return {"income": None}
        except ValueError:
            dispatcher.utter_message(text="Please enter a valid numeric income.")
            return {"income": None}


class ActionSubmitHealthPolicyForm(Action):
    """
    A Rasa custom action for submitting the Health Policy form.

    This action collects the validated user input from the Health Policy form,
    formats the information into a payload, and submits it using the `create_user` function.
    It also handles the response and potential errors, providing feedback to the user.
    """

    def name(self) -> Text:
        """
        Returns the name of the action.

        This method is used by Rasa to identify the action by its name.

        Returns:
            str: The name of the action, "action_submit_health_policy_form".
        """
        return "action_submit_health_policy_form"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """
        Executes the action for submitting the Health Policy form.

        This method retrieves user data from the slots, formats it into a payload,
        and sends it to the `create_user` function. It then constructs a message with
        the submitted information and sends it to the user. In case of an error,
        it provides an error message to the user.

        Args:
            dispatcher (CollectingDispatcher): The dispatcher used to send messages back to the user.
            tracker (Tracker): The tracker that keeps track of the conversation state.
            domain (Dict[Text, Any]): The domain dictionary containing the bot's intents, actions, etc.

        Returns:
            List[Dict[Text, Any]]: A list of slot updates. All slots related to the Health Policy form are reset to `None`.
        """
        name = tracker.get_slot('name')
        email = tracker.get_slot('email')
        age = tracker.get_slot('age')
        phone_number = tracker.get_slot('phone_number')
        income = tracker.get_slot('income')
        
        payload = {
            "username": name,
            "email": email,
            "age": age,
            "phone_number": phone_number,
            "income": income
        }
        try:
            result = create_user(payload)
            message = (
                "🔍 Here's the information About you:\n"
                f"👤 *Username:* {result['username']}\n"
                f"📧 *Email:* {result['email']}\n"
                f"🎂 *Age:* {result['age']}\n"
                f"📞 *Phone Number:* {result['phone_number']}\n"
                f"💼 *Income:* {result['income']}\n"
            )
            buttons = get_main_menu_buttons()

            dispatcher.utter_message(text=message, buttons=buttons)
        except requests.exceptions.RequestException as e:
            dispatcher.utter_message(text=f"Failed to submit form: {str(e)}")
        
        return [
            SlotSet('name', None),
            SlotSet('email', None),
            SlotSet('age', None),
            SlotSet('phone_number', None),
            SlotSet('income', None)
        ]


class ActionUserDetails(Action):
    """
    A Rasa custom action for retrieving and displaying user details.

    This action fetches user data based on the provided phone number, extracts
    relevant details, and constructs a message to inform the user. If the user data
    cannot be retrieved, it prompts the user to update their details.
    """

    def name(self) -> Text:
        """
        Returns the name of the action.

        This method is used by Rasa to identify the action by its name.

        Returns:
            str: The name of the action, "action_user_details".
        """
        return "action_user_details"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """
        Executes the action for retrieving and displaying user details.

        This method retrieves the phone number from the slot, fetches the user data,
        and sends a message with the user's details. If the user data cannot be found,
        it prompts the user to update their details and initiates a form to collect missing information.

        Args:
            dispatcher (CollectingDispatcher): The dispatcher used to send messages back to the user.
            tracker (Tracker): The tracker that keeps track of the conversation state.
            domain (Dict[Text, Any]): The domain dictionary containing the bot's intents, actions, etc.

        Returns:
            List[Dict[Text, Any]]: An empty list if user details are retrieved, or a list containing a `FollowupAction` to prompt for details if user data is not found.
        """
        print("inside the Action User Details")
        phone_number = tracker.get_slot('phone_number')
        print(f"phone_number: {phone_number}")

        if phone_number:
            user_data = fetch_user_data(phone_number)
        
            if user_data:
                username, email, age, income = extract_user_details(user_data)

                message = (
                    f"Hello,\n \n"
                    "👋 I'm VISoF Buddy, your trusted WhatsApp Insurance Assistant. I'm here to help you with all your insurance needs and provide you with the best assistance.\n \n"
                    "🔍 Here's the information About you:\n"
                    f"👤 *Username:* {username}\n"
                    f"📧 *Email:* {email}\n"
                    f"🎂 *Age:* {age}\n"
                    f"📞 *Phone Number:* {phone_number}\n"
                    f"💼 *Income:* {income}\n"
                )
                buttons = get_update_and_confirm_data_buttons()

                dispatcher.utter_message(text=message, buttons=buttons)
                return []
            
            else:
                message = (
                    "🚫 We're unable to retrieve your details at the moment. To ensure we have accurate information, please update your details. \n \n"
                    "📋 Kindly enter your *name* below to proceed."
                )

                dispatcher.utter_message(text=message)
                return [
                    FollowupAction("user_details_form")
                ]


class ActionAddUser(Action):
    """
    A Rasa custom action for initiating the user addition process.

    This action prompts the user to provide their name as the first step in the process
    of adding a new user. It sends a message asking for the user's name and waits for
    the user's response.
    """

    def name(self) -> Text:
        """
        Returns the name of the action.

        This method is used by Rasa to identify the action by its name.

        Returns:
            str: The name of the action, "action_add_user".
        """
        return "action_add_user"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """
        Executes the action to prompt the user for their name.

        This method sends a message to the user asking for their name, which is the initial
        step in adding a new user. It does not process any data or update any slots at
        this stage.

        Args:
            dispatcher (CollectingDispatcher): The dispatcher used to send messages back to the user.
            tracker (Tracker): The tracker that keeps track of the conversation state.
            domain (Dict[Text, Any]): The domain dictionary containing the bot's intents, actions, etc.

        Returns:
            List[Dict[Text, Any]]: An empty list, as this action only sends a message and does not require any additional action.
        """
        message = "Please, can you tell me your name?"
        dispatcher.utter_message(text=message)
        return []


class ActionUpdateUserDetails(Action):
    """
    A Rasa custom action for providing options to update user details.

    This action sends a message to the user, presenting options for updating different
    user details. The user can choose to update their username, email, age, or income.
    """

    def name(self) -> Text:
        """
        Returns the name of the action.

        This method is used by Rasa to identify the action by its name.

        Returns:
            str: The name of the action, "action_update_user_details".
        """
        return "action_update_user_details"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """
        Executes the action to prompt the user with options for updating their details.

        This method retrieves the phone number from the slot and sends a message to the
        user with buttons to update various details. The user can choose to update their
        username, email, age, or income.

        Args:
            dispatcher (CollectingDispatcher): The dispatcher used to send messages back to the user.
            tracker (Tracker): The tracker that keeps track of the conversation state.
            domain (Dict[Text, Any]): The domain dictionary containing the bot's intents, actions, etc.

        Returns:
            List[Dict[Text, Any]]: An empty list, as this action only sends a message with options and does not perform additional actions.
        """
        phone_number = tracker.get_slot('phone_number')
        print(f"Get Update User Details Phone Number: {phone_number}")

        if phone_number:
            message = "Please let me know which field you'd like to update:"
            buttons = [
                {"title": "Update Username", "payload": "/update_username_details"},
                {"title": "Update Email", "payload": "/update_email_details"},
                {"title": "Update Age", "payload": "/update_age_details"},
                {"title": "Update Income", "payload": "/update_income_details"},
            ]
            dispatcher.utter_message(text=message, buttons=buttons)

        return []


class ActionConfirmUserDetails(Action):
    """
    A Rasa custom action to confirm user details and present the main menu.

    This action retrieves the phone number and user name from the slots and sends a
    confirmation message to the user with buttons to access the main menu.
    """

    def name(self) -> Text:
        """
        Returns the name of the action.

        This method is used by Rasa to identify the action by its name.

        Returns:
            str: The name of the action, "action_confirm_user_details".
        """
        return "action_confirm_user_details"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """
        Executes the action to confirm user details and present the main menu.

        This method retrieves the phone number and user name from the slots. If the phone
        number is available, it sends a confirmation message to the user with buttons to
        access the main menu.

        Args:
            dispatcher (CollectingDispatcher): The dispatcher used to send messages back to the user.
            tracker (Tracker): The tracker that keeps track of the conversation state.
            domain (Dict[Text, Any]): The domain dictionary containing the bot's intents, actions, etc.

        Returns:
            List[Dict[Text, Any]]: An empty list, as this action only sends a confirmation message with buttons
            and does not perform additional actions.
        """
        phone_number = tracker.get_slot("phone_number")
        user_name = tracker.get_slot("name")
        
        if phone_number:
            message = get_main_menu_message()
            buttons = get_main_menu_buttons()
            dispatcher.utter_message(text=message, buttons=buttons)

        return []


class ActionUpdateUsernameDetails(Action):
    """
    A Rasa custom action to handle updating the username details for a user.

    This action retrieves the phone number from the slot, fetches the user's current username,
    and prompts the user to provide a new username.
    """

    def name(self) -> Text:
        """
        Returns the name of the action.

        This method is used by Rasa to identify the action by its name.

        Returns:
            str: The name of the action, "action_update_username_details".
        """
        return "action_update_username_details"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """
        Executes the action to update the user's username details.

        This method retrieves the phone number from the slot, fetches the user's current username
        using the phone number, and sends a message to prompt the user to provide a new username.

        Args:
            dispatcher (CollectingDispatcher): The dispatcher used to send messages back to the user.
            tracker (Tracker): The tracker that keeps track of the conversation state.
            domain (Dict[Text, Any]): The domain dictionary containing the bot's intents, actions, etc.

        Returns:
            List[Dict[Text, Any]]: An empty list, as this action only sends a message and does not perform
            additional actions.
        """
        phone_number = tracker.get_slot('phone_number')

        if phone_number:
            user_data = fetch_user_data(phone_number)
            if user_data:
                username = user_data.get('username')
                dispatcher.utter_message(
                    text=f"Your 👤 *username*: *{username}* \n \n Please provide the new username:"
                )
                
        return []


class ValidateUpdateUsernameDetailsForm(FormValidationAction):
    """
    A Rasa custom validation action for validating the username update form.

    This action validates the new username provided by the user, ensuring that it meets the criteria.
    It handles failed attempts and provides appropriate messages to guide the user.
    """

    def name(self) -> Text:
        """
        Returns the name of the validation action.

        This method is used by Rasa to identify the action by its name.

        Returns:
            str: The name of the action, "validate_update_username_details_form".
        """
        return "validate_update_username_details_form"

    def validate_update_username(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> List[Dict[Text, Any]]:
        """
        Validates the new username provided by the user.

        This method checks if the username is valid (alphabetic) and handles failed attempts.
        If the username is valid, it is returned. Otherwise, an appropriate message is sent to the user,
        and the number of failed attempts is tracked.

        Args:
            slot_value (Any): The value of the slot being validated.
            dispatcher (CollectingDispatcher): The dispatcher used to send messages back to the user.
            tracker (Tracker): The tracker that keeps track of the conversation state.
            domain (DomainDict): The domain dictionary containing the bot's intents, actions, etc.

        Returns:
            List[Dict[Text, Any]]: A list of slot values to set. This includes the validated username or a fallback value
            if validation fails. It also includes the updated number of failed attempts if needed.
        """
        update_username = tracker.get_slot('update_username').strip().lower()
        phone_number = tracker.get_slot('phone_number')

        print(f"update_username_value: {update_username}")

        if phone_number:
            failed_attempts = tracker.get_slot('failed_attempts') or 0

            if update_username.isalpha():
                return {"update_username": update_username}
            else:
                failed_attempts += 1
                if failed_attempts == 3:
                    get_update_user = {"update_username": "fallback", "failed_attempts": None}
                    print(f"get_update_user::::{get_update_user}")
                    return get_update_user
                else:
                    dispatcher.utter_message(text="Please enter a valid username.")
                    attempts_value = {"failed_attempts": failed_attempts, "update_username": None}
                    print(f"failed_attempts_value: {attempts_value}")
                    return attempts_value


class SubmitUpdateUsernameDetailsForm(Action):
    """
    A Rasa custom action for submitting the updated username details form.

    This action handles the submission of the updated username, including calling the update API,
    fetching the updated user data, and sending the appropriate response to the user.
    """

    def name(self) -> Text:
        """
        Returns the name of the action.

        This method is used by Rasa to identify the action by its name.

        Returns:
            str: The name of the action, "submit_update_username_details_form".
        """
        return "submit_update_username_details_form"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """
        Executes the action to submit updated username details.

        This method checks if the username is set to "fallback" or a valid value, then performs
        the appropriate actions. If the username is valid, it updates the user's details via an API,
        fetches the updated user data, and sends a response to the user with the updated information.
        If the username is "fallback", it fetches and displays the user's current details.

        Args:
            dispatcher (CollectingDispatcher): The dispatcher used to send messages back to the user.
            tracker (Tracker): The tracker that keeps track of the conversation state.
            domain (Dict[Text, Any]): The domain dictionary containing the bot's intents, actions, etc.

        Returns:
            List[Dict[Text, Any]]: A list of slot updates. This includes resetting the "update_username" slot.
        """
        phone_number = tracker.get_slot("phone_number")
        update_username = tracker.get_slot('update_username')

        if phone_number:
            print(f"update_username_value: {update_username}")
            if update_username == "fallback":
                user_data = fetch_user_data(phone_number)
                if user_data:
                    username, email, age, income = extract_user_details(user_data)
                    
                    message = get_user_info_message(username, email, age, phone_number, income)
                    buttons = get_update_and_confirm_data_buttons()

                    dispatcher.utter_message(text=message, buttons=buttons) 
                    return [SlotSet("update_username", None)]   

            else:
                # Call the Update API
                payload = {
                    "username": update_username
                }
                user_data = update_user_details(phone_number, payload)
                name = user_data.get('username', '')
                email = user_data.get('email', '')
                age = user_data.get('age', '')
                phone_number = user_data.get('phone_number', '')
                income = user_data.get('income', '')

                message = (
                    "Hello,\n \n"
                    "👋 I'm VISoF Buddy, your trusted WhatsApp Insurance Assistant. I'm here to help you with all your insurance needs and provide you with the best assistance. \n \n"
                    "🔍 Here's the *Updated* information about you: \n"
                    f"👤 *Username:* {name}\n"
                    f"📧 *Email:* {email}\n"
                    f"🎂 *Age:* {age}\n"
                    f"📞 *Phone Number:* {phone_number}\n"
                    f"💼 *Income:* {income}\n"
                )
                buttons = get_update_and_confirm_data_buttons()

                dispatcher.utter_message(text=message, buttons=buttons)
                return [SlotSet("update_username", None)]


class ActionUpdateEmailDetails(Action):
    """
    A Rasa custom action for initiating the email update process.

    This action retrieves the user's current email and prompts them to provide a new email address.
    """

    def name(self) -> Text:
        """
        Returns the name of the action.

        This method is used by Rasa to identify the action by its name.

        Returns:
            str: The name of the action, "action_update_email_details".
        """
        return "action_update_email_details"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """
        Executes the action to initiate the email update process.

        This method retrieves the user's current email from the slot and prompts the user to provide a new email address.
        If the phone number is available, it fetches the user data and sends a message with the current email,
        asking for the new email address.

        Args:
            dispatcher (CollectingDispatcher): The dispatcher used to send messages back to the user.
            tracker (Tracker): The tracker that keeps track of the conversation state.
            domain (Dict[Text, Any]): The domain dictionary containing the bot's intents, actions, etc.

        Returns:
            List[Dict[Text, Any]]: An empty list, as no slot updates are made by this action.
        """
        phone_number = tracker.get_slot('phone_number')

        if phone_number:
            user_data = fetch_user_data(phone_number)
            if user_data:
                email = user_data.get('email')
                dispatcher.utter_message(
                    text=f"Your 📧 *email*: *{email}* \n \n Please provide the new email address:"
                )
                return []


class ValidateUpdateEmailDetailsForm(FormValidationAction):
    """
    A Rasa custom action for validating the email update form.

    This action validates the new email address provided by the user to ensure it meets the required format.
    It handles retries and fallback cases if the user fails to provide a valid email after multiple attempts.
    """

    def name(self) -> Text:
        """
        Returns the name of the validation action.

        This method is used by Rasa to identify the validation action by its name.

        Returns:
            str: The name of the action, "validate_update_email_details_form".
        """
        return "validate_update_email_details_form"

    def validate_update_email(self,
                              slot_value: Any,
                              dispatcher: CollectingDispatcher,
                              tracker: Tracker,
                              domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """
        Validates the new email address provided by the user.

        This method checks if the provided email address is valid (contains '@' and '.' and has a length greater than 7).
        It also manages failed attempts and provides feedback to the user. If the user fails to provide a valid email
        after three attempts, the slot is set to "fallback" and failed attempts are reset.

        Args:
            slot_value (Any): The value of the slot being validated.
            dispatcher (CollectingDispatcher): The dispatcher used to send messages back to the user.
            tracker (Tracker): The tracker that keeps track of the conversation state.
            domain (Dict[Text, Any]): The domain dictionary containing the bot's intents, actions, etc.

        Returns:
            List[Dict[Text, Any]]: A list containing the validated slot value or fallback value if the maximum attempts are reached.
        """
        phone_number = tracker.get_slot('phone_number')
        update_email = tracker.get_slot('update_email').strip().lower()

        print(f"update_email_value: {update_email}")

        if phone_number:
            failed_attempts = tracker.get_slot('failed_attempts') or 0

            if "@" in update_email and "." in update_email and len(update_email) > 7:
                return {"update_email": update_email}
            else:
                failed_attempts += 1
                if failed_attempts == 3:
                    get_update_email = {"update_email": "fallback", "failed_attempts": None}
                    print(f"get_update_email::::{get_update_email}")
                    return get_update_email
                else:
                    dispatcher.utter_message(text="Please enter a valid email.")
                    attempts_value = {"failed_attempts": failed_attempts, "update_email": None}
                    print(f"failed_attempts_value: {attempts_value}")
                    return attempts_value


class SubmitUpdateEmailDetailsForm(Action):
    """
    A Rasa custom action for submitting the updated email details.

    This action handles the submission of the updated email address provided by the user. It manages the update process
    by calling an external API and then provides feedback to the user with updated information. It also handles cases
    where the user enters a fallback value.
    """

    def name(self) -> Text:
        """
        Returns the name of the action for submitting email details.

        This method is used by Rasa to identify the action by its name.

        Returns:
            str: The name of the action, "submit_update_email_details_form".
        """
        return "submit_update_email_details_form"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
        ) -> List[Dict[Text, Any]]:
        """
        Executes the action to submit the updated email details.

        This method retrieves the updated email address from the slot, cleans it, and checks if it is a fallback value.
        If it's not a fallback value, it updates the user's email through an external API. If it is a fallback value, 
        it fetches and displays the user's existing details and provides options to update or confirm the information.

        Args:
            dispatcher (CollectingDispatcher): The dispatcher used to send messages back to the user.
            tracker (Tracker): The tracker that keeps track of the conversation state.
            domain (Dict[Text, Any]): The domain dictionary containing the bot's intents, actions, etc.

        Returns:
            List[Dict[Text, Any]]: A list containing the slot updates. Specifically, the "update_email" slot is set to None.
        """
        phone_number = tracker.get_slot("phone_number")
        update_email = tracker.get_slot('update_email').lower()

        if phone_number:
            update_email = re.sub(r'\s+', '', update_email)
            print(f"updated_email: {update_email}")

            if update_email == "fallback":
                user_data = fetch_user_data(phone_number)

                if user_data:
                    username, email, age, income = extract_user_details(user_data)

                    message = get_user_info_message(username, email, age, phone_number, income)
                    buttons = get_update_and_confirm_data_buttons()

                    dispatcher.utter_message(text=message, buttons=buttons) 
                    return [SlotSet("update_email", None)]

            else:
                # Call the Update API
                payload = {
                    "email": update_email
                }
                user_data = update_user_details(phone_number, payload)
                name = user_data.get('username', '')
                email = user_data.get('email', '')
                age = user_data.get('age', '')
                phone_number = user_data.get('phone_number', '')
                income = user_data.get('income', '')
                
                message = (
                    "Hello,\n \n"
                    "👋 I'm VISoF Buddy, your trusted WhatsApp Insurance Assistant. I'm here to help you with all your insurance needs and provide you with the best assistance. \n \n"
                    "🔍 Here's the *Updated* information about you: \n"
                    f"👤 *Username:* {name}\n"
                    f"📧 *Email:* {email}\n"
                    f"🎂 *Age:* {age}\n"
                    f"📞 *Phone Number:* {phone_number}\n"
                    f"💼 *Income:* {income}\n"
                )
                buttons = get_update_and_confirm_data_buttons()

                dispatcher.utter_message(text=message, buttons=buttons)
                return [SlotSet("update_email", None)]


class ActionUpdateAgeDetails(Action):
    """
    A Rasa custom action for updating the user's age details.

    This action prompts the user to provide their new age. It retrieves the current age from the user data
    and requests the user to provide an updated age value.
    """

    def name(self) -> Text:
        """
        Returns the name of the action for updating age details.

        This method is used by Rasa to identify the action by its name.

        Returns:
            str: The name of the action, "action_update_age_details".
        """
        return "action_update_age_details"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
        ) -> List[Dict[Text, Any]]:
        """
        Executes the action to update the user's age details.

        This method retrieves the current age from the user's data based on their phone number and sends a message
        to the user requesting their new age. If the phone number is present, it fetches the user data and constructs
        a message to prompt the user for their new age.

        Args:
            dispatcher (CollectingDispatcher): The dispatcher used to send messages back to the user.
            tracker (Tracker): The tracker that keeps track of the conversation state.
            domain (Dict[Text, Any]): The domain dictionary containing the bot's intents, actions, etc.

        Returns:
            List[Dict[Text, Any]]: An empty list as no slot updates are made in this action.
        """
        phone_number = tracker.get_slot('phone_number')

        if phone_number:
            user_data = fetch_user_data(phone_number)
            if user_data:
                age = user_data.get('age')
                dispatcher.utter_message(text=f"Your 🎂 *Age*: *{age}* \n \n Please provide the new age:")
                return []

        return []


class ValidateUpdateAgeDetailsForm(FormValidationAction):
    """
    A Rasa form validation action for validating the user's age update.

    This action validates the age provided by the user. It checks that the age is a positive integer between 1 and 120.
    If the age is valid, it updates the slot; otherwise, it prompts the user to provide a valid age.
    """

    def name(self) -> Text:
        """
        Returns the name of the validation action for updating age details.

        This method is used by Rasa to identify the validation action by its name.

        Returns:
            str: The name of the validation action, "validate_update_age_details_form".
        """
        return "validate_update_age_details_form"

    def validate_update_age(self,
                            slot_value: Any,
                            dispatcher: CollectingDispatcher,
                            tracker: Tracker,
                            domain: Dict[Text, Any]
        ) -> List[Dict[Text, Any]]:
        """
        Validates the user's input for the age update.

        This method checks whether the provided age is a positive integer between 1 and 120. If the input is valid,
        it returns the updated age; otherwise, it returns a message prompting the user to enter a valid age.

        Args:
            slot_value (Any): The value provided by the user for the age slot.
            dispatcher (CollectingDispatcher): The dispatcher used to send messages back to the user.
            tracker (Tracker): The tracker that keeps track of the conversation state.
            domain (Dict[Text, Any]): The domain dictionary containing the bot's intents, actions, etc.

        Returns:
            List[Dict[Text, Any]]: A list containing the updated age or fallback action in case of multiple failed attempts.
        """
        phone_number = tracker.get_slot('phone_number')
        update_age = tracker.get_slot('update_age').strip()

        print(f"update_age: {update_age}")

        if phone_number:
            failed_attempts = tracker.get_slot('failed_attempts') or 0

            if update_age.isdigit() and 0 < int(update_age) <= 120:
                return {"update_age": update_age}
            else:
                failed_attempts += 1
                if failed_attempts == 3:
                    return {"update_age": "fallback", "failed_attempts": None}
                else:
                    dispatcher.utter_message(text="Please enter a valid age.")
                    return {"failed_attempts": failed_attempts, "update_age": None}


class SubmitUpdateAgeDetailsForm(Action):
    """
    A Rasa action for submitting the updated age details provided by the user.

    This action handles the final submission of the updated age provided by the user. If the age update is valid, 
    it calls the update API to update the user's details and then sends a message with the updated information.
    If the update is not valid, it returns the user to the previous step or provides a fallback option.
    """

    def name(self) -> Text:
        """
        Returns the name of the action for submitting the updated age details.

        This method is used by Rasa to identify the action by its name.

        Returns:
            str: The name of the action, "submit_update_age_details_form".
        """
        return "submit_update_age_details_form"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
        ) -> List[Dict[Text, Any]]:
        """
        Handles the submission of the updated age details.

        This method checks the provided age, and if it's valid, it updates the user's details through an API call.
        It then sends a message with the updated user information and provides the user with buttons for further actions.
        If the update is not valid, it handles fallback and resets the slot.

        Args:
            dispatcher (CollectingDispatcher): The dispatcher used to send messages back to the user.
            tracker (Tracker): The tracker that keeps track of the conversation state.
            domain (Dict[Text, Any]): The domain dictionary containing the bot's intents, actions, etc.

        Returns:
            List[Dict[Text, Any]]: A list containing the updated slot or the reset slot in case of fallback.
        """
        phone_number = tracker.get_slot("phone_number")
        if phone_number:
            update_age = tracker.get_slot('update_age')
            print(f"update_age: {update_age}")

            if update_age == "fallback":
                user_data = fetch_user_data(phone_number)
                if user_data:
                    username, email, age, income = extract_user_details(user_data)

                    message = get_user_info_message(username, email, age, phone_number, income)
                    buttons = get_update_and_confirm_data_buttons()

                    dispatcher.utter_message(text=message, buttons=buttons) 
                    return [SlotSet("update_age", None)]

            else:
                # Call the Update API
                payload = {"age": update_age}
                user_data = update_user_details(phone_number, payload)
                name = user_data.get('username', '')
                email = user_data.get('email', '')
                age = user_data.get('age', '')
                phone_number = user_data.get('phone_number', '')
                income = user_data.get('income', '')

                message = (
                    "Hello,\n \n"
                    "👋 I'm VISoF Buddy, your trusted WhatsApp Insurance Assistant. I'm here to help you with all your insurance needs and provide you with the best assistance. \n \n"
                    "🔍 Here's the *Updated* information about you: \n"
                    f"👤 *Username:* {name}\n"
                    f"📧 *Email:* {email}\n"
                    f"🎂 *Age:* {age}\n"
                    f"📞 *Phone Number:* {phone_number}\n"
                    f"💼 *Income:* {income}\n"
                )
                buttons = get_update_and_confirm_data_buttons()

                dispatcher.utter_message(text=message, buttons=buttons)
                return [SlotSet("update_age", None)]


class ActionUpdateIncomeDetails(Action):
    """
    A Rasa action for initiating the update of user income details.

    This action retrieves the current income of the user based on their phone number and prompts the user
    to provide the new income amount. The action assumes that the phone number slot is correctly set and
    valid user data can be fetched.
    """

    def name(self) -> Text:
        """
        Returns the name of the action for updating income details.

        This method is used by Rasa to identify the action by its name.

        Returns:
            str: The name of the action, "action_update_income_details".
        """
        return "action_update_income_details"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
        ) -> List[Dict[Text, Any]]:
        """
        Retrieves the current income details and prompts the user to provide new income information.

        This method checks if the phone number slot is set, fetches the user data using the phone number,
        and retrieves the current income. It then sends a message to the user asking for the new income amount.

        Args:
            dispatcher (CollectingDispatcher): The dispatcher used to send messages back to the user.
            tracker (Tracker): The tracker that keeps track of the conversation state.
            domain (Dict[Text, Any]): The domain dictionary containing the bot's intents, actions, etc.

        Returns:
            List[Dict[Text, Any]]: An empty list, indicating that no slots need to be set or updated in this action.
        """
        phone_number = tracker.get_slot('phone_number')

        if phone_number:
            user_data = fetch_user_data(phone_number)
            if user_data:
                income = user_data.get('income')
                dispatcher.utter_message(text=f"Your 💼 *Income*: *{income}* \n \n Please provide the new Income:")
                return []


class ValidateUpdateIncomeDetailsForm(FormValidationAction):
    """
    A Rasa FormValidationAction for validating the income update form.

    This validation action ensures that the provided income value is valid before it is accepted.
    It checks if the income value is a positive integer. If the user fails to provide valid input
    after three attempts, the action will return a fallback value.
    """

    def name(self) -> Text:
        """
        Returns the name of the form validation action.

        This method is used by Rasa to identify the validation action by its name.

        Returns:
            str: The name of the validation action, "validate_update_income_details_form".
        """
        return "validate_update_income_details_form"

    def validate_update_income(self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
        ) -> List[Dict[Text, Any]]:
        """
        Validates the provided income value.

        This method checks if the provided income value is a positive integer. If the value is valid,
        it returns the updated income. If the value is invalid, it increments the failed attempts counter.
        After three failed attempts, it returns a fallback value and resets the counter.

        Args:
            slot_value (Any): The value to be validated for the income slot.
            dispatcher (CollectingDispatcher): The dispatcher used to send messages back to the user.
            tracker (Tracker): The tracker that keeps track of the conversation state.
            domain (Dict[Text, Any]): The domain dictionary containing the bot's intents, actions, etc.

        Returns:
            List[Dict[Text, Any]]: A list containing the updated slot value if valid, or a fallback value
                                    after three failed attempts.
        """
        phone_number = tracker.get_slot('phone_number')
        update_income = tracker.get_slot('update_income').strip()

        print(f"update_income: {update_income}")

        if phone_number:
            failed_attempts = tracker.get_slot('failed_attempts') or 0

            if update_income.isdigit() and int(update_income) > 0:
                return {"update_income": update_income}
            else:
                failed_attempts = failed_attempts + 1
                if failed_attempts == 3:
                    get_update_income = {"update_income": "fallback", "failed_attempts": None}
                    print(f"get_update_income: {get_update_income}")
                    return get_update_income
                else:
                    dispatcher.utter_message(text="Please enter a valid income.")
                    attempts_value = {"failed_attempts": failed_attempts, "update_income": None}
                    print(f"failed_attempts_value: {attempts_value}")
                    return attempts_value


class SubmitUpdateIncomeDetailsForm(Action):
    """
    A Rasa Action for submitting the updated income details form.

    This action handles the submission of the updated income provided by the user. It updates the user's
    income in the database and sends a message with the updated information. If the user has failed to
    provide valid input and a fallback is triggered, it retrieves and displays the current user information.
    """

    def name(self) -> Text:
        """
        Returns the name of the action for submitting the updated income details form.

        This method is used by Rasa to identify the action by its name.

        Returns:
            str: The name of the action, "submit_update_income_details_form".
        """
        return "submit_update_income_details_form"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
        ) -> List[Dict[Text, Any]]:
        """
        Executes the action to submit the updated income details.

        This method checks if the income update is a fallback or a valid value. If it is a fallback,
        it retrieves the current user data and sends a message with the user's updated information.
        If a valid income is provided, it updates the user's income in the database and sends
        a message with the updated user details.

        Args:
            dispatcher (CollectingDispatcher): The dispatcher used to send messages back to the user.
            tracker (Tracker): The tracker that keeps track of the conversation state.
            domain (Dict[Text, Any]): The domain dictionary containing the bot's intents, actions, etc.

        Returns:
            List[Dict[Text, Any]]: A list containing the SlotSet action to clear the update_income slot.
        """
        phone_number = tracker.get_slot("phone_number")

        if phone_number:
            update_income = tracker.get_slot('update_income')
            print(f"update_income: {update_income}")

            if update_income == "fallback":
                user_data = fetch_user_data(phone_number)

                if user_data:
                    username, email, age, income = extract_user_details(user_data)

                    message = get_user_info_message(username, email, age, phone_number, income)
                    buttons = get_update_and_confirm_data_buttons()

                    dispatcher.utter_message(text=message, buttons=buttons)
                    return [SlotSet("update_income", None)]

            else:
                # Call the Update API
                payload = {
                    "income": update_income
                }
                user_data = update_user_details(phone_number, payload)
                name = user_data.get('username', '')
                email = user_data.get('email', '')
                age = user_data.get('age', '')
                phone_number = user_data.get('phone_number', '')
                income = user_data.get('income', '')
                message = (
                    "Hello,\n \n"
                    "👋 I'm VISoF Buddy, your trusted WhatsApp Insurance Assistant. I'm here to help you with all your insurance needs and provide you with the best assistance. \n \n"
                    "🔍 Here's the *Updated* information about you: \n"
                    f"👤 *Username:* {name}\n"
                    f"📧 *Email:* {email}\n"
                    f"🎂 *Age:* {age}\n"
                    f"📞 *Phone Number:* {phone_number}\n"
                    f"💼 *Income:* {income}\n"
                )
                buttons = get_update_and_confirm_data_buttons()

                dispatcher.utter_message(text=message, buttons=buttons)
                return [SlotSet("update_income", None)]


class ValidateUserDetailsForm(FormValidationAction):
    """
    A Rasa FormValidationAction for validating user details.

    This action validates various user details provided during form submission. It checks the validity of
    the user's name, email, age, phone number, and income, providing appropriate feedback and ensuring
    that only valid data is accepted.
    """

    def name(self) -> Text:
        """
        Returns the name of the form validation action.

        This method is used by Rasa to identify the action by its name.

        Returns:
            str: The name of the action, "validate_user_details_form".
        """
        return "validate_user_details_form"

    def validate_name(self,
                      slot_value: Any,
                      dispatcher: CollectingDispatcher,
                      tracker: Tracker,
                      domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """
        Validates the 'name' slot value.

        This method ensures that the provided name is a valid string consisting of alphabetical characters
        and has a length greater than one.

        Args:
            slot_value (Any): The value to validate for the 'name' slot.
            dispatcher (CollectingDispatcher): The dispatcher used to send messages back to the user.
            tracker (Tracker): The tracker that keeps track of the conversation state.
            domain (Dict[Text, Any]): The domain dictionary containing the bot's intents, actions, etc.

        Returns:
            List[Dict[Text, Any]]: A list containing the updated 'name' slot value or `None` if invalid.
        """
        name = tracker.get_slot('name').lower()
        print(f"This is name: {name}")

        if name.replace(" ", "").isalpha() and len(name) > 1:
            dispatcher.utter_message(text="Thanks! Now, could you please provide your email?")
            return {"name": name}
        else:
            dispatcher.utter_message(text="Please enter a valid name.")
            return {"name": None}

    def validate_email(self,
                       slot_value: Any,
                       dispatcher: CollectingDispatcher,
                       tracker: Tracker,
                       domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """
        Validates the 'email' slot value.

        This method ensures that the provided email contains "@" and "." and has a length greater than seven.

        Args:
            slot_value (Any): The value to validate for the 'email' slot.
            dispatcher (CollectingDispatcher): The dispatcher used to send messages back to the user.
            tracker (Tracker): The tracker that keeps track of the conversation state.
            domain (Dict[Text, Any]): The domain dictionary containing the bot's intents, actions, etc.

        Returns:
            List[Dict[Text, Any]]: A list containing the updated 'email' slot value or `None` if invalid.
        """
        get_email = tracker.get_slot('email').strip().lower()
        email = re.sub(r'\s+', '', get_email)
        print(f"This is email: {email}")

        if "@" in email and "." in email and len(email) > 7:
            dispatcher.utter_message(text="Thanks! Now, could you please provide your age?")
            return {"email": email}
        else:
            dispatcher.utter_message(text="Please enter a valid email address.")
            return {"email": None}

    def validate_age(self,
                     slot_value: Any,
                     dispatcher: CollectingDispatcher,
                     tracker: Tracker,
                     domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """
        Validates the 'age' slot value.

        This method ensures that the provided age is a digit and falls within the range of 1 to 120.

        Args:
            slot_value (Any): The value to validate for the 'age' slot.
            dispatcher (CollectingDispatcher): The dispatcher used to send messages back to the user.
            tracker (Tracker): The tracker that keeps track of the conversation state.
            domain (Dict[Text, Any]): The domain dictionary containing the bot's intents, actions, etc.

        Returns:
            List[Dict[Text, Any]]: A list containing the updated 'age' slot value or `None` if invalid.
        """
        age = tracker.get_slot('age')
        print(f"This is age: {age}")

        if age and age.isdigit() and 0 < int(age) <= 120:
            dispatcher.utter_message(text="Thanks! Now, could you please provide your Income?")
            return {"age": age}
        else:
            dispatcher.utter_message(text="Please enter a valid age.")
            return {"age": None}

    def validate_phone_number(self,
                              slot_value: Any,
                              dispatcher: CollectingDispatcher,
                              tracker: Tracker,
                              domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """
        Validates the 'phone_number' slot value.

        This method ensures that the provided phone number is numeric and does not exceed 15 digits.

        Args:
            slot_value (Any): The value to validate for the 'phone_number' slot.
            dispatcher (CollectingDispatcher): The dispatcher used to send messages back to the user.
            tracker (Tracker): The tracker that keeps track of the conversation state.
            domain (Dict[Text, Any]): The domain dictionary containing the bot's intents, actions, etc.

        Returns:
            List[Dict[Text, Any]]: A list containing the updated 'phone_number' slot value or `None` if invalid.
        """
        phone_number = tracker.get_slot('phone_number')
        print(f"This is Phone Number: {phone_number}")

        if phone_number.isdigit() and len(phone_number) <= 15:
            return {"phone_number": phone_number}
        else:
            dispatcher.utter_message(text="Please enter a valid phone number.")
            return {"phone_number": None}

    def validate_income(self,
                        slot_value: Any,
                        dispatcher: CollectingDispatcher,
                        tracker: Tracker,
                        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """
        Validates the 'income' slot value.

        This method ensures that the provided income is a valid numeric value greater than zero.

        Args:
            slot_value (Any): The value to validate for the 'income' slot.
            dispatcher (CollectingDispatcher): The dispatcher used to send messages back to the user.
            tracker (Tracker): The tracker that keeps track of the conversation state.
            domain (Dict[Text, Any]): The domain dictionary containing the bot's intents, actions, etc.

        Returns:
            List[Dict[Text, Any]]: A list containing the updated 'income' slot value or `None` if invalid.
        """
        income = tracker.get_slot('income')
        print(f"This is Income: {income}")

        try:
            income_value = float(income)
            if income_value > 0:
                return {"income": income}
            else:
                dispatcher.utter_message(text="Please enter a valid income.")
                return {"income": None}
        except ValueError:
            dispatcher.utter_message(text="Please enter a valid numeric income.")
            return {"income": None}


class ActionSubmitUserDetailsForm(Action):
    """
    A Rasa action for submitting user details from a form.

    This action collects user details from the form slots, creates a user with these details, and sends
    a confirmation message back to the user with the submitted information and update options.
    """

    def name(self) -> Text:
        """
        Returns the name of the action.

        This method is used by Rasa to identify the action by its name.

        Returns:
            str: The name of the action, "action_submit_user_details_form".
        """
        return "action_submit_user_details_form"
    
    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """
        Handles the submission of user details from the form.

        This method retrieves the values from the form slots, creates a user with these details, and sends
        a confirmation message to the user. It also provides options for updating the information.

        Args:
            dispatcher (CollectingDispatcher): The dispatcher used to send messages back to the user.
            tracker (Tracker): The tracker that keeps track of the conversation state.
            domain (Dict[Text, Any]): The domain dictionary containing the bot's intents, actions, etc.

        Returns:
            List[Dict[Text, Any]]: An empty list, as the method does not need to return any additional events.
        """
        
        print("Submit Form Data:::::::::::")

        # Retrieve slot values
        name = tracker.get_slot('name')
        email = tracker.get_slot('email')
        age = tracker.get_slot('age')
        phone_number = tracker.get_slot('phone_number')
        income = tracker.get_slot('income')

        # Print slot values for debugging
        print(f"name: {name}")
        print(f"email: {email}")
        print(f"age: {age}")
        print(f"phone_number: {phone_number}")
        print(f"income: {income}")
        
        # Prepare payload for user creation
        payload = {
            "username": name,
            "email": email,
            "age": age,
            "phone_number": phone_number,
            "income": income
        }

        # Create user with the provided details
        result = create_user(payload)
        print(f"result: {result}")

        # Prepare and send confirmation message
        message = (
            "Hello,\n \n"
            "👋 I'm VISoF Buddy, your trusted WhatsApp Insurance Assistant. I'm here to help you with all your insurance needs and provide you with the best assistance.\n \n"
            "🔍 Here's the information about you:\n"
            f"👤 *Username:* {result['username']}\n"
            f"📧 *Email:* {result['email']}\n"
            f"🎂 *Age:* {result['age']}\n"
            f"📞 *Phone Number:* {result['phone_number']}\n"
            f"💼 *Income:* {result['income']}\n"
        )
        buttons = get_update_and_confirm_data_buttons()

        dispatcher.utter_message(text=message, buttons=buttons)
        return []


class ActionGetAllUser(Action):
    """
    A Rasa action for retrieving and displaying details of all users.

    This action fetches user data from a data source, formats it into a message, and sends it to the user.
    It handles large messages by splitting them into chunks and sending them separately if necessary.
    """

    def name(self) -> Text:
        """
        Returns the name of the action.

        This method is used by Rasa to identify the action by its name.

        Returns:
            str: The name of the action, "action_get_all_user".
        """
        return "action_get_all_user"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """
        Retrieves all user data and sends it to the user in chunks if necessary.

        This method fetches user data, formats it into a readable message, and handles message length by
        splitting it into chunks if it exceeds a maximum length. It sends each chunk separately and
        provides a main menu for navigation.

        Args:
            dispatcher (CollectingDispatcher): The dispatcher used to send messages back to the user.
            tracker (Tracker): The tracker that keeps track of the conversation state.
            domain (Dict[Text, Any]): The domain dictionary containing the bot's intents, actions, etc.

        Returns:
            List[Dict[Text, Any]]: An empty list, as the method does not need to return any additional events.
        """
        
        # Fetch all user data
        user_data = fetch_all_user_data()
        buttons = get_main_menu_buttons()

        # Maximum message length for splitting
        max_message_length = 1500

        if user_data:
            # Build user details message
            user_details_message = "User Details:\n"
            for user in user_data:
                user_details_message += (
                    # f"ID: {user['id']}\n"
                    f"Username: {user['username']}\n"
                    f"Email: {user['email']}\n"
                    f"Age: {user['age']}\n"
                    f"Phone Number: {user['phone_number']}\n"
                    f"Income: {user['income']}\n"
                    f"-------------------------\n \n \n"
                )
            
            # Split message into chunks if necessary
            while len(user_details_message) > max_message_length:
                chunk = user_details_message[:max_message_length]
                print("chunk::::::::::::::::::::", chunk)
                dispatcher.utter_message(text=chunk, buttons=buttons)
                user_details_message = user_details_message[max_message_length:]
            
            # Send the remaining part of the message
            dispatcher.utter_message(text=user_details_message, buttons=buttons)
        else:
            dispatcher.utter_message(text="Failed to retrieve user details.")

        return []

