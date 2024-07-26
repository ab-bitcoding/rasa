from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction
from rasa_sdk.types import DomainDict
import requests
import re
from utils.utils import create_user

class ActionGreetUser(Action):

    def name(self) -> Text:
        return "action_greet_user"

    def run(self, 
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        message = (
            "Great! We found 1 Garage near you. Given below are the details of workshops: \n \n"
            "*Superon* \n"
            "Tele No : 9876543211 \n \n"
            "*Safdarjang* \n"
            "Tele No : 8765432123 \n \n"
            "Click below link to view garages on map: \n \n"
            "https://dxa2.jcowk/oxwo=jcwojcown \n \n"
            "If you require any assistance, \n \n" 
            "Call - *1800XXXXXXXXX* \n"
            "Missed call and get callback: \n"
            "9876543211"
        )

        buttons = [
            {"title": "English", "payload": '/select_language{"language":"english"}'},
            {"title": "Hindi", "payload": '/select_language{"language":"hindi"}'}
        ]

        dispatcher.utter_message(text=message, buttons=buttons)

        return []


class ActionSelectLanguage(Action):

    def name(self) -> Text:
        return "action_select_language"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

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
            message = "Need help with renewal, claims or any other insurance-related support."
            buttons = [
                {"title": "Main Menu", "payload": '/select_menu_item'}
                ]

            dispatcher.utter_message(text=message,buttons=buttons)
            return [SlotSet("language", normalized_language)]


class ActionMenuList(Action):
    def name(self) -> Text:
        return "action_menu_list"
    
    def run(self,
            dispatcher:CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            message = (
                "Need help with renewal, claims, or any other insurance-related support. \n \n"
                "Click on *Main Menu*"
            )
            buttons = [
                {"title": "Renew Policy", "payload": '/renew_policy'},
                {"title": "Claims Related", "payload": '/claims_related'},
                {"title": "Download Policy Copy", "payload": '/download_policy'},
                {"title": "Emergengy Support", "payload": '/emergency_support'},
                {"title": "Nearly Workshop", "payload": '/near_by_workshop'},
                {"title": "New Policy", "payload": '/new_policy'},
                {"title": "Health Policy", "payload": '/health_policy'},
                {"title": "User Details", "payload": '/user_details'}

            ]

            dispatcher.utter_message(text=message, buttons=buttons)

            return []


class ActionEmergencySupport(Action):
    def name(self) -> Text:
        return "action_emergency_support"
    
    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
            message = (
                "In case you need repair service, enter the pincode and share your current location to connect with the nearest workshop. \n \n"
                "If you require any assistance, \n \n"
                "Call - *1800XXXXXXXXX* \n"
                "Missed call and get a callback: \n"
                "9876543211"
            )
            dispatcher.utter_message(text=message)
            return []


class ActionNearByWorkshop(Action):
    def name(self) -> Text:
        return "action_near_by_workshop"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker:Tracker,
            domain:Dict[Text, Any]) -> List[Dict[Text, Any]]:
        message = (
            "🙂 We are happy to assist you.\n \n"
            "Please enter the Pincode or share your current location."
        )

        dispatcher.utter_message(text=message)
        return []


class ActionRenewPolicy(Action):
    def name(self) -> Text:
        return "action_renew_policy"
    
    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
            message = (
                """
                Renew Policy
                """
            )
            dispatcher.utter_message(text=message)
            return []


class ActionUserDetails(Action):
    def name(self) -> Text:
        return "action_user_details"
    
    def run(self,
            dispatcher:CollectingDispatcher,
            tracker:Tracker,
            domain: Dict[Text,Any]
            
    ) -> List[Dict[Text, Any]]:
        
        message  = (
            "User Details Submission Form"
        )
        buttons = [
            {"title": "Add User", "payload": '/add_user{"user_action":"adduser"}'},
            {"title": "Update User", "payload": '/update_user{"user_action":"updateuser"}'},
            {"title": "Get All User", "payload": '/get_all_user{"user_action":"getalluser"}'}
        ]
        dispatcher.utter_message(text=message, buttons=buttons)
        return []
    
    def format_user_details(self, user_data: List[Dict[str, Any]]) -> Text:
        # Format the user details for display
        if not user_data:
            return "No users found."
        
        user_details = []
        for user in user_data:
            details = f"User ID: {user.get('id')}, Name: {user.get('name')}, Email: {user.get('email')}"
            user_details.append(details)
        
        return "\n".join(user_details)


class ValidateEmergencySupportPincodeForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_emergency_support_pincode_form"

    def validate_pincode(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        print("Emergency Validation Function Running")
        emergency_pincode = str(slot_value)
        print(f"emergency_pincode: {emergency_pincode}")
        if len(emergency_pincode) == 6 and emergency_pincode.isdigit():
            return {"pincode": emergency_pincode}
        else:
            message = (
                "Looks like the location is invalid. \n \n"
                "Please enter the pincode or share your current location." 
            )
            dispatcher.utter_message(text=message)
            return {"pincode": None}


class ActionSubmitEmergencyPincodeForm(Action):
    def name(self) -> Text:
        return "action_submit_emergency_support_pincode_form"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: "DomainDict") -> List[Dict[Text, Any]]:
        emergency_pincode = tracker.get_slot("pincode")
        print("emergency_pincode::::",emergency_pincode)
        if emergency_pincode:
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
            buttons = [
                {"title": "Main Menu", "payload": '/select_menu_item'}
            ]
            dispatcher.utter_message(text=message, buttons=buttons)
        else:
            message = ( 
                "Looks like the location is invalid.\n"
                "Please enter the pincode or share your current location" 
            )
            dispatcher.utter_message(text=message)

        return [SlotSet("pincode", None)]


class ValidaeNearByWorkshopPincodeForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_near_by_workshop_pincode_form"
    
    def validate_pincode(
            self,
            slot_value:Any,
            dispatcher: CollectingDispatcher,
            tracker:Tracker,
            domain:Dict[Text, Any]) -> List[Dict[Text, Any]]:
        near_by_workshop_pincode_value = str(slot_value)

        if len(near_by_workshop_pincode_value) == 6 and near_by_workshop_pincode_value.isdigit():
            return {"pincode": near_by_workshop_pincode_value}
        else:
            message = (
                "Looks like the location is invalid. \n \n"
                "Please enter the pincode or share your current location" 
            )
            dispatcher.utter_message(text=message)
            return {"pincode": None}


class ActionSubmitNearByWorkshopPincodeForm(Action):
    def name(self) -> Text:
        return "action_submit_near_by_workshop_pincode_form"
    
    def run(
            self,
            dispatcher:CollectingDispatcher,
            tracker:Tracker,
            domain: "DomainDict") -> List[Dict[Text, Any]]:
        near_by_workshop_pincode = tracker.get_slot("pincode")
        if near_by_workshop_pincode:
            message = (
                "Great! We found 1 Garage near you. Given below are the details of workshops: \n \n"
                "*Superon* \n"
                "Tele No: 9876543211 \n \n"
                "*Safdarjang* \n"
                "Tele No : 8765432123 \n \n"
                "Click the link below to view garages on the map: \n"
                "https://dxa2.jcowk/oxwo=jcwojcown \n \n"
                "If you require any assistance, \n \n"
                "Call - *1800XXXXXXXXX* \n"
                "Missed call and get a callback: \n"
                "9876543211"
            )
            buttons = [
                {"title": "Main Menu", "payload": '/select_menu_item'}
            ]
            dispatcher.utter_message(text=message, buttons=buttons)
        else:
            message = ("""
                Looks like the location is invalid.

                Please enter the pincode or share your current location 
            """)
            dispatcher.utter_message(text=message)
        return [SlotSet("pincode", None)]


class ActionHealthPolicy(Action):
    def name(self) -> Text:
        """Returns the name of the action."""
        return "action_health_policy"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """Executes the action."""
        
        message = (
            "You are now in the Health Policy section. \n \n"
            "Please fill out the form for the Health Policy. \n \n"
            "We need some details to proceed with your request. Thank you! \n \n"
            "Please enter your name"
        )
        dispatcher.utter_message(text=message)
        return []


class ValidateHealthPolicyForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_health_policy_form"

    def validate_name(self,
                      slot_value:Any,
                      dispatcher:CollectingDispatcher,
                      tracker: Tracker,
                      domain: Dict[Text,Any]) -> List[Dict[Text, Any]]:

        name = tracker.get_slot('name').lower()
        print(f"This is name: {name}")
        if name.replace(" ", "").isalpha() and len(name) > 1:
            dispatcher.utter_message(text="Thanks! Now, could you please provide your email?")
            return {"name": name}
        else:
            dispatcher.utter_message(text="Please enter a valid name.")
            return {"name": None}

    def validate_email(self,
                       slot_value:Any,
                      dispatcher:CollectingDispatcher,
                      tracker: Tracker,
                      domain: Dict[Text,Any]) -> List[Dict[Text, Any]]:
        

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
                    slot_value:Any,
                    dispatcher:CollectingDispatcher,
                    tracker: Tracker,
                    domain: Dict[Text,Any]) -> List[Dict[Text, Any]]:

        age  = tracker.get_slot('age')
        print(f"This is age: {age}")
        if age.isdigit() and 0 < int(age) <= 120:
            dispatcher.utter_message(text="Thanks! Now, could you please provide your Phone Number?") 
            return {"age": age}
        else:
            dispatcher.utter_message(text="Please enter a valid age")
            return {"age": None}

    def validate_phone_number(self,
                    slot_value: Any,
                    dispatcher:CollectingDispatcher,
                    tracker: Tracker,
                    domain: Dict[Text,Any]) -> List[Dict[Text, Any]]:

        phone_number = tracker.get_slot('phone_number')
        print(f"This is Phone Number: {phone_number}")
        if phone_number.isdigit() and len(phone_number) == 10:
            dispatcher.utter_message(text="Thanks! Now, could you please provide your Income?") 
            return {"phone_number": phone_number}
        else:
            dispatcher.utter_message(text="Please enter a valid phone number")
            return {"phone_number": None}

    def validate_income(self,
                    slot_value:Any,
                    dispatcher:CollectingDispatcher,
                    tracker: Tracker,
                    domain: Dict[Text,Any]) -> List[Dict[Text, Any]]:

        income = tracker.get_slot('income').strip()
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
    def name(self) -> Text:
        return "action_submit_health_policy_form"
    
    def run(self,
            dispatcher: CollectingDispatcher,
            tracker:Tracker,
            domain:Dict[Text, Any]) -> List[Dict[Text, Any]]:
        name = tracker.get_slot('name')
        email = tracker.get_slot('email')
        age = tracker.get_slot('age')
        phone_number = tracker.get_slot('phone_number')
        income = tracker.get_slot('income')

        message = (
            f"*Details of the Form:* \n \n"
            f"Your name is *{name}* \n"
            f"Your email is {email} \n"
            f"Your age is *{age}* \n"
            f"Your Phone Number is {phone_number} \n"
            f"Your Income is {income}"
        )
        buttons = [
                {"title": "Main Menu", "payload": '/select_menu_item'}
            ]
        dispatcher.utter_message(text=message, buttons=buttons)
        
        payload = {
            "username": name,
            "email": email,
            "age": age,
            "phone_number": phone_number,
            "income": income
        }
        try:
            result = create_user(payload)
            dispatcher.utter_message(text=f"Form submitted successfully! ID: {result['id']}")
        except requests.exceptions.RequestException as e:
            dispatcher.utter_message(text=f"Failed to submit form: {str(e)}")
        return [
            SlotSet('name', None),
            SlotSet('email', None),
            SlotSet('age', None),
            SlotSet('phone_number', None),
            SlotSet('income', None)
        ]

class ActionGetAllUser(Action):
    def name(self) -> Text:
        return "action_get_all_user"
    
    def run(self,
            dispatcher:CollectingDispatcher,
            tracker:Tracker,
            domain:Dict[Text,Any]
    ) -> List[Dict[Text, Any]]:
        
        user_action = tracker.get_slot("getalluser")
        if user_action == 'getalluser':
            api_url = "https://your-api-endpoint.com/get_all_users"
            response = requests.get(api_url)
            if response.status_code == 200:
                user_data = response.json()
                user_details_message = self.format_user_details(user_data)
                dispatcher.utter_message(text=user_details_message)
            else:
                dispatcher.utter_message(text="Failed to retrieve user details.")

        return []


