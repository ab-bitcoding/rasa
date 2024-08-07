import os
from dotenv import load_dotenv

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction
from rasa_sdk.types import DomainDict
import requests
import re
from utils.utils import create_user, fetch_user_data, fetch_all_user_data, update_user_details
from channels.whatsapp import WhatsAppOutput 
load_dotenv()

class ActionGreetUser(Action):
    def name(self) -> Text:
        return "action_greet_user"

    def run(self, 
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Retrieve the mobile number from metadata
        metadata = tracker.latest_message.get('metadata', {})
        user_phone_number = metadata.get("sender")
        print(f"greet user_phone_number: {user_phone_number}")

        if user_phone_number:
            user_data = fetch_user_data(user_phone_number)
            if user_data:
                name  = user_data.get('username')
                email  = user_data.get('email')
                age  = user_data.get('age')
                income  = user_data.get('income')

                message = (
                    f"Hello, \n \n"
                    "👋 I'm VISoF Buddy, your trusted WhatsApp Insurance Assistant. I'm here to help you with all your insurance needs and provide you with the best assistance. \n \n"
                    "🔍 Here's the information About you:\n"
                    f"👤 *Username:* {name}\n"
                    f"📧 *Email:* {email}\n"
                    f"🎂 *Age:* {age}\n"
                    f"📞 *Phone Number:* {user_phone_number}\n"
                    f"💼 *Income:* {income}\n"
                    "-------------------------\n \n"
                    "To ensure we have the correct information, please select one of the options below: \n \n"
                    "🔄 If any details need updating, click on the *Update* button.\n"
                    "✅ If the information is correct, click on the *Confirm* button.\n \n"
                    "We're here to assist you with any questions or concerns. Your satisfaction is our priority!\n \n"
                    "Best regards,\n"
                    "VISoF Buddy Team"
                )

                buttons = [
                    {"title": "Update", "payload": '/update_user_details'},
                    {"title": "Confirm", "payload": '/confirm_user_details'}
                ]

                dispatcher.utter_message(text=message, buttons=buttons)
                return [
                    SlotSet("phone_number", user_phone_number),
                    SlotSet("name", name),
                    SlotSet("email", email),
                    SlotSet("age", age),
                    SlotSet("income", income)
                ]

            else:
                message = (
                    "🚫 We're unable to retrieve your details at the moment. To ensure we have accurate information, please update your details. \n \n"
                    "📋 Kindly enter your name below to proceed."
                )

                dispatcher.utter_message(text=message)
                return [
                    SlotSet("phone_number", user_phone_number),
                    FollowupAction("user_details_form")
                ]


class ActionConfirmUserDetails(Action):
    def name(self) -> Text:
        return "action_confirm_user_details"
    
    def run(self,
            dispatcher:CollectingDispatcher,
            tracker:Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text,Any]]:
        
        phone_number = tracker.get_slot("phone_number")
        user_name = tracker.get_slot("name")
        if phone_number:
            message = (
                f"Hi {user_name},\n \n"
                "I am VISoF Buddy, your WhatsApp Insurance Assistant. \n \n"
                "Your Hyundai Verna (DL - 3CBU - 6767) Insurance Policy (Policy No: 3423223276548663) is valid until 28 Feb 2024. \n \n"
                "Let's get started with your renewal, claims, or any other insurance-related support you might need. Feel free to reach out for assistance! \n \n"
                "Best regards,\n"
                "VISoF Buddy Team"
            )
            buttons = [
                {"title": "Renew Policy", "payload": '/renew_policy'},
                {"title": "Claims Related", "payload": '/claims_related'},
                {"title": "Download Policy Copy", "payload": '/download_policy'},
                {"title": "Emergengy Support", "payload": '/emergency_support'},
                {"title": "Nearly Workshop", "payload": '/near_by_workshop'},
                {"title": "New Policy", "payload": '/new_policy'},
                {"title": "Health Policy", "payload": '/health_policy'},
                {"title": "User Details", "payload": '/user_details'},
                {"title": "Update User Details", "payload": '/update_user_details'}
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
            {"title": "Add User", "payload": '/add_user'},
            {"title": "Update User", "payload": '/update_user'},
            {"title": "Get All User", "payload": '/get_all_user'}
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


class ActionAddUser(Action):
    def name(self) -> Text:
        return "action_add_user"
    
    def run(self,
            dispatcher:CollectingDispatcher,
            tracker:Tracker,
            domian: Dict[Text,Any]) -> List[Dict[Text,Any]]:
        message = ("Please, Can you tell me your Name")
        dispatcher.utter_message(text=message)
        return []


class ActionUpdateUserDetails(Action):
    def name(self) -> Text:
        return "action_update_user_details"
    
    def run(self,
            dispatcher:CollectingDispatcher,
            tracker:Tracker,
            domain: Dict[Text,Any]) -> List[Dict[Text,Any]]:
        
        phone_number = tracker.get_slot('phone_number')
        print(f"Get Update User Details Phone Number: {phone_number}")

        if phone_number:

            message = (
                "Please let me know which field you'd like to update:"
            )
            buttons = [
                {"title": "Update Username", "payload" : "/update_username_details"},
                {"title": "Update Email", "payload" : "/update_email_details"},
                {"title": "Update Age", "payload" : "/update_age_details"},
                {"title": "Update Income", "payload" : "/update_income_details"},
            ]
            dispatcher.utter_message(text=message, buttons=buttons)

            return []


class ActionUpdateUsernameDetails(Action):
    def name(self) -> Text:
        return "action_update_username_details"
    
    def run(self,
            dispatcher:CollectingDispatcher,
            tracker:Tracker,
            domain:Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        phone_number = tracker.get_slot('phone_number')

        if phone_number:
                user_data = fetch_user_data(phone_number)
                if user_data:
                    username = user_data.get('username')
                    dispatcher.utter_message(text=f"Your 👤 *username*: *{username}* \n \n Please provide the new username:")
                    return []


class ValidateUpdateUsernameDetailsForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_update_username_details_form"
    
    def validate_update_username(self,
            slot_value: Any,
            dispatcher:CollectingDispatcher,
            tracker:Tracker,
            domain: DomainDict) -> List:
        
        update_username = tracker.get_slot('update_username').strip().lower()
        phone_number = tracker.get_slot('phone_number')

        print(f"update_username_value: {update_username}")

        if phone_number:
            failed_attempts = tracker.get_slot('failed_attempts') or 0

            if update_username.isalpha():
                return {"update_username": update_username}
            else:
                failed_attempts = failed_attempts + 1
                if failed_attempts == 3:
                    get_update_user = {"update_username" :"fallback","failed_attempts": None}
                    print(f"get_update_user::::{get_update_user}")
                    return get_update_user
                else:
                    dispatcher.utter_message(text="Please enter a valid username.")
                    attemps_value = {"failed_attempts": failed_attempts,"update_username": None}
                    print(f"failed_attemps_value: {attemps_value}")
                    return attemps_value


class SubmitUpdateUsernameDetailsForm(Action):
    def name(self) -> Text:
        return "submit_update_username_details_form"
    
    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain:Dict[Text, Any]
        ) -> List[Dict[Text, Any]]:

        phone_number = tracker.get_slot("phone_number")
        update_username = tracker.get_slot('update_username')

        if phone_number:
            print(f"update_username_value: {update_username}")
            if update_username == "fallback":
                user_data = fetch_user_data(phone_number)
                if user_data:
                    username = user_data.get('username')
                    email = user_data.get('email') 
                    age = user_data.get('age')
                    income = user_data.get('income')

                    message = (
                    "Having trouble updating the data? 🔄 Use the *Update* and *Confirm* button. Let us know if you need help. 🤝 \n \n"
                    "🔍 Here's the information About you:\n"
                    f"👤 *Username:* {username} \n"
                    f"📧 *Email:* {email} \n"
                    f"🎂 *Age:* {age} \n"
                    f"📞 *Phone Number:* {phone_number} \n"
                    f"💼 *Income:* {income} \n"
                    )
                    buttons = [
                        {"title": "Update", "payload": '/update_user_details'},
                        {"title": "Confirm", "payload": '/confirm_user_details'}
                    ]

                    dispatcher.utter_message(text=message, buttons=buttons) 
                    return [SlotSet("update_username", None)]   

            else:
                ## Call the Update API ##
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
                buttons = [
                    {"title": "Update", "payload": '/update_user_details'},
                    {"title": "Confirm", "payload": '/confirm_user_details'}
                ]

                dispatcher.utter_message(text=message, buttons=buttons)
                return [SlotSet("update_username", None)]


class ActionUpdateEmailDetails(Action):
    def name(self) -> Text:
        return "action_update_email_details"
    
    def run(self,
            dispatcher:CollectingDispatcher,
            tracker:Tracker,
            domain:Dict[Text,Any])-> List[Dict[Text, Any]]:
        
        phone_number = tracker.get_slot('phone_number')

        if phone_number:
                user_data = fetch_user_data(phone_number)
                if user_data:
                    email = user_data.get('email')
                    dispatcher.utter_message(text=f"Your 📧 *email*: *{email}* \n \n Please provide the new email address:")
                    return []


class ValidateUpdateEmailDetailsForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_update_email_details_form"
    
    def validate_update_email(self,
            slot_vlaue: Any,
            dispatcher:CollectingDispatcher,
            tracker:Tracker,
            domain:Dict[Text, Any]) -> List[Dict[Text,Any]]:
        
        phone_number = tracker.get_slot('phone_number')
        update_email = tracker.get_slot('update_email').strip().lower()

        print(f"update_email_value: {update_email}")

        if phone_number:
            failed_attempts = tracker.get_slot('failed_attempts') or 0
            if "@" in update_email and "." in update_email and len(update_email) > 7:
                return {"update_email": update_email}
            else:
                failed_attempts = failed_attempts + 1
                if failed_attempts == 3:
                    get_update_email = {"update_email" :"fallback","failed_attempts": None}
                    print(f"get_update_email::::{get_update_email}")
                    return get_update_email
                else:
                    dispatcher.utter_message(text="Please enter a valid email.")
                    attemps_value = {"failed_attempts": failed_attempts,"update_email": None}
                    print(f"failed_attemps_value: {attemps_value}")
                    return attemps_value


class SubmitUpdateEmailDetailsForm(Action):
    def name(self) -> Text:
        return "submit_update_email_details_form"
    
    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain:Dict[Text, Any]
        ) -> List[Dict[Text, Any]]:

        phone_number = tracker.get_slot("phone_number")
        update_email = tracker.get_slot('update_email').lower()

        if phone_number:
            update_email = re.sub(r'\s+', '', update_email)
            print(f"updated_email: {update_email}")

            if update_email == "fallback":
                user_data = fetch_user_data(phone_number)

                if user_data:
                    username = user_data.get('username')
                    email = user_data.get('email') 
                    age = user_data.get('age')
                    income = user_data.get('income')

                    message = (
                    "Having trouble updating the data? 🔄 Use the *Update* and *Confirm* button. Let us know if you need help. 🤝 \n \n"
                    "🔍 Here's the information About you:\n"
                    f"👤 *Username:* {username} \n"
                    f"📧 *Email:* {email} \n"
                    f"🎂 *Age:* {age} \n"
                    f"📞 *Phone Number:* {phone_number} \n"
                    f"💼 *Income:* {income} \n"
                    )
                    buttons = [
                        {"title": "Update", "payload": '/update_user_details'},
                        {"title": "Confirm", "payload": '/confirm_user_details'}
                    ]

                    dispatcher.utter_message(text=message, buttons=buttons) 
                    return [SlotSet("update_email", None)]

            else:
                ## Call the Update API
                payload = {
                    "email":update_email
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
                buttons = [
                    {"title": "Update", "payload": '/update_user_details'},
                    {"title": "Confirm", "payload": '/confirm_user_details'}
                ]
                dispatcher.utter_message(text=message, buttons=buttons)
                empty_update_email_slot = SlotSet("update_email", None)
                return [empty_update_email_slot]


class ActionUpdateAgeDetails(Action):
    def name(self) -> Text:
        return "action_update_age_details"
    
    def run(self,
            dispatcher:CollectingDispatcher,
            tracker:Tracker,
            domain:Dict[Text,Any])-> List[Dict[Text, Any]]:
        
        phone_number = tracker.get_slot('phone_number')

        if phone_number:
                user_data = fetch_user_data(phone_number)
                if user_data:
                    age = user_data.get('age')
                    dispatcher.utter_message(text=f"Your 🎂 *Age*: *{age}* \n \n Please provide the new age:")
                    return []


class ValidateUpdateAgeDetailsForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_update_age_details_form"
    
    def validate_update_age(self,
            slot_vlaue: Any,
            dispatcher:CollectingDispatcher,
            tracker:Tracker,
            domain:Dict[Text, Any]) -> List[Dict[Text,Any]]:
        
        phone_number = tracker.get_slot('phone_number')
        update_age = tracker.get_slot('update_age').strip()

        print(f"update_age: {update_age}")

        if phone_number:
            failed_attempts = tracker.get_slot('failed_attempts') or 0

            if update_age.isdigit() and 0 < int(update_age) <= 120:
                return {"update_age": update_age}
            else:
                failed_attempts = failed_attempts + 1
                if failed_attempts == 3:
                    get_update_age = {"update_age" :"fallback","failed_attempts": None}
                    print(f"get_update_age: {get_update_age}")
                    return get_update_age
                else:
                    dispatcher.utter_message(text="Please enter a valid age.")
                    attemps_value = {"failed_attempts": failed_attempts,"update_age": None}
                    print(f"failed_attemps_value: {attemps_value}")
                    return attemps_value



class SubmitUpdateAgeDetailsForm(Action):
    def name(self) -> Text:
        return "submit_update_age_details_form"
    
    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain:Dict[Text, Any]
        ) -> List[Dict[Text, Any]]:

        phone_number = tracker.get_slot("phone_number")
        if phone_number:
            update_age = tracker.get_slot('update_age')
            print(f"update_age: {update_age}")
            if update_age == "fallback":
                user_data = fetch_user_data(phone_number)

                if user_data:
                    username = user_data.get('username')
                    email = user_data.get('email') 
                    age = user_data.get('age')
                    income = user_data.get('income')

                    message = (
                    "Having trouble updating the data? 🔄 Use the *Update* and *Confirm* button. Let us know if you need help. 🤝 \n \n"
                    "🔍 Here's the information About you:\n"
                    f"👤 *Username:* {username} \n"
                    f"📧 *Email:* {email} \n"
                    f"🎂 *Age:* {age} \n"
                    f"📞 *Phone Number:* {phone_number} \n"
                    f"💼 *Income:* {income} \n"
                    )
                    buttons = [
                        {"title": "Update", "payload": '/update_user_details'},
                        {"title": "Confirm", "payload": '/confirm_user_details'}
                    ]

                    dispatcher.utter_message(text=message, buttons=buttons) 
                    return [SlotSet("update_age", None)]

            else:
                ## Call the Update API
                payload = {
                    "age":update_age
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
                buttons = [
                    {"title": "Update", "payload": '/update_user_details'},
                    {"title": "Confirm", "payload": '/confirm_user_details'}
                ]
                dispatcher.utter_message(text=message, buttons=buttons)
                empty_update_age_slot = SlotSet("update_age", None)
                return [empty_update_age_slot]


class ActionUpdateIncomeDetails(Action):
    def name(self) -> Text:
        return "action_update_income_details"
    
    def run(self,
            dispatcher:CollectingDispatcher,
            tracker:Tracker,
            domain:Dict[Text,Any])-> List[Dict[Text, Any]]:
        
        phone_number = tracker.get_slot('phone_number')
        income = tracker.get_slot("income")

        if phone_number:
                dispatcher.utter_message(text=f"Your 💼 *Income*: *{income}* \n \n Please provide the new Income:")
                return []


class ValidateUpdateIncomeDetailsForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_update_income_details_form"
    
    def validate_update_income(self,
            slot_vlaue: Any,
            dispatcher:CollectingDispatcher,
            tracker:Tracker,
            domain:Dict[Text, Any]) -> List[Dict[Text,Any]]:
        
        phone_number = tracker.get_slot('phone_number')
        if phone_number:
            update_income = tracker.get_slot('update_income').strip()

            if update_income.isdigit() and int(update_income) > 0:
                return {"update_income": update_income}
            else:
                dispatcher.utter_message(text="Please enter a valid income.")
            return {"update_income": None}


class SubmitUpdateIncomeDetailsForm(Action):
    def name(self) -> Text:
        return "submit_update_income_details_form"
    
    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
        ) -> List[Dict[Text, Any]]:

        phone_number = tracker.get_slot("phone_number")
        if phone_number:
            updated_income = tracker.get_slot('update_income')
            print(f"updated_income: {updated_income}")
            ## Call the Update API
            payload = {
                "income": updated_income
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
            buttons = [
                {"title": "Update", "payload": '/update_user_details'},
                {"title": "Confirm", "payload": '/confirm_user_details'}
            ]
            dispatcher.utter_message(text=message, buttons=buttons)
            empty_update_income_slot = SlotSet("update_income", None)
            return [empty_update_income_slot]


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
        if age and 0 < int(age) <= 120:
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
        if phone_number.isdigit() and len(phone_number) <= 15:
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


class ValidateUserDetailsForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_user_details_form"

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

        age = tracker.get_slot('age')
        print(f"This is age: {age}")
        if age and 0 < int(age) <= 120:
            dispatcher.utter_message(text="Thanks! Now, could you please provide your Income?")
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
        if phone_number.isdigit() and len(phone_number) <= 15:
            # dispatcher.utter_message(text="Thanks! Now, could you please provide your Income?")
            return {"phone_number": phone_number}
        else:
            dispatcher.utter_message(text="Please enter a valid phone number")
            return {"phone_number": None}

    def validate_income(self,
                    slot_value:Any,
                    dispatcher:CollectingDispatcher,
                    tracker: Tracker,
                    domain: Dict[Text,Any]) -> List[Dict[Text, Any]]:

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
        except requests.exceptions.RequestException as e:
            dispatcher.utter_message(text=f"Failed to submit form: {str(e)}")
        return [
            SlotSet('name', None),
            SlotSet('email', None),
            SlotSet('age', None),
            SlotSet('phone_number', None),
            SlotSet('income', None)
        ]


class ActionSubmitUserDetailsForm(Action):
    def name(self) -> Text:
        return "action_submit_user_details_form"
    
    def run(self,
            dispatcher: CollectingDispatcher,
            tracker:Tracker,
            domain:Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        print("Submit Form Data:::::::::::")

        name = tracker.get_slot('name')
        email = tracker.get_slot('email')
        age = tracker.get_slot('age')
        phone_number = tracker.get_slot('phone_number')
        income = tracker.get_slot('income')

        print(f"name: {name}")
        print(f"email: {email}")
        print(f"age: {age}")
        print(f"phone_number: {phone_number}")
        print(f"income: {income}")
        
        
        payload = {
            "username": name,
            "email": email,
            "age": age,
            "phone_number": phone_number,
            "income": income
        }

        result = create_user(payload)
        print(f"result: {result}")

        message = (
        f"Hello,\n \n"
        "👋 I'm VISoF Buddy, your trusted WhatsApp Insurance Assistant. I'm here to help you with all your insurance needs and provide you with the best assistance.\n \n"
        "🔍 Here's the information About you:\n"
        f"👤 *Username:* {result['username']}\n"
        f"📧 *Email:* {result['email']}\n"
        f"🎂 *Age:* {result['age']}\n"
        f"📞 *Phone Number:* {result['phone_number']}\n"
        f"💼 *Income:* {result['income']}\n"
        )

        buttons = [
            {"title": "Update", "payload": '/update_user_details'},
            {"title": "Confirm", "payload": '/confirm_user_details'}
        ]
        dispatcher.utter_message(text=message, buttons=buttons)
        return [
            # SlotSet('name', None),
            # SlotSet('email', None),
            # SlotSet('age', None),
            # SlotSet('phone_number', None),
            # SlotSet('income', None)
        ]


class ActionGetAllUser(Action):
    def name(self) -> Text:
        return "action_get_all_user"

    def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_data = fetch_all_user_data()
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
        max_message_length = 1500
        if user_data:
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

