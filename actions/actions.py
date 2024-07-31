import os
from dotenv import load_dotenv

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction
from rasa_sdk.types import DomainDict
import requests
import re
from utils.utils import create_user, fetch_user_data, fetch_all_user_data
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
        print("user_phone_number:::::::::;;", user_phone_number)

        if user_phone_number:
            user_data = fetch_user_data(user_phone_number)
            name  = user_data.get('username')
            email  = user_data.get('email')
            age  = user_data.get('age')
            income  = user_data.get('income')
            message = (
                f"Hello,\n \n"
                "👋 I'm VISoF Buddy, your trusted WhatsApp Insurance Assistant. I'm here to help you with all your insurance needs and provide you with the best assistance. \n \n"
                "🔍 Here's the information About you :\n"
                f"👤 *Username:* {name}\n"
                f"📧 *Email:* {email}\n"
                f"🎂 *Age:* {age}\n"
                f"📞 *Phone Number:* {user_phone_number}\n"
                f"💼 *Income:* {income}\n"
                "-------------------------\n \n"
                "To ensure we have the correct information, please select one of the options below:\n \n"
                "🔄 If any details need updating, click on the *Update* button.\n"
                "✅ If the information is correct, click on the *Confirm* button. \n \n"
                "We're here to assist you with any questions or concerns. Your satisfaction is our priority! \n \n"
                "Best regards,\n"
                "VISoF Buddy Team"
            )

            buttons = [
                {"title": "Update", "payload": '/update_user'},
                {"title": "Confirm", "payload": '/confirm_user'}
            ]

            dispatcher.utter_message(text=message, buttons=buttons)
            return [
                SlotSet("phone_number", user_phone_number),
                SlotSet("name", name),
                SlotSet("email",email),
                SlotSet('age', age),
                SlotSet('phone_number', user_phone_number),
                SlotSet('income', income)
            ]
        
        else:
            # If the phone number is not provided, send a different message
            message = (
                "Hi, it seems we couldn't retrieve your phone number. \n \n"
                "Please provide your phone number to proceed with assistance. \n \n"
                "You can also select your language preference for further communication."
            )

            buttons = [
                {"title": "Main Menu", "payload": '/select_menu_item}'}
            ]

            dispatcher.utter_message(text=message, buttons=buttons)
            return [SlotSet("phone_number", None)]

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
                {"title": "Main Menu", "payload": '/select_menu_item'}
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


# class ActionUpdateUser(Action):
#     def name(self) -> Text:
#         return "action_update_user"
    
#     def run(deslf,
#             dispatcher:CollectingDispatcher,
#             tracker:Tracker,
#             domain:Dict[Text,Any])-> List[Dict[Text,Any]]:
#         update_field = tracker.get_slot('update_field')
#         update_value = tracker.get_slot('update_value')
#         print("update_field::::",update_field)
#         if not update_field:
#             # Prompt the user to specify which field they want to update
#             dispatcher.utter_message(
#                 text="Which field would you like to update? Please choose from the following: Name, Email, Age, Phone Number, or Income."
#             )
#             return []
        
#         current_data = {
#             'name': tracker.get_slot('name'),
#             'email': tracker.get_slot('email'),
#             'age': tracker.get_slot('age'),
#             'phone_number': tracker.get_slot('phone_number'),
#             'income': tracker.get_slot('income')
#         }
#         print("current_data::::",current_data)


#         if update_field.lower() not in current_data:
#             dispatcher.utter_message(text="Invalid field. Please choose a valid field to update.")
#             return []

#         # Display the current value of the specified field
#         dispatcher.utter_message(
#             text=f"The current value for {update_field} is: {current_data[update_field.lower()]}. Please provide the new value."
#         )

#         if not update_value:
#             # Prompt for the new value if not provided
#             dispatcher.utter_message(
#                 text=f"Please provide the new value for {update_field}."
#             )
#             return []
        
#          # Update the slot with the new value
#         tracker.slots[update_field.lower()] = update_value


#         # user_phone_number = tracker.get_slot('phone_number')
#         # username = tracker.get_slot('username')
#         # print("username::::", username)
#         # email = tracker.get_slot('email')
#         # print("email::::", email)
#         # age = tracker.get_slot('age')
#         # print("age::::", age)
#         # # phone_number = tracker.get_slot('phone_number')
#         # income = tracker.get_slot('income')
#         # print("income::::", income)


#         if not user_phone_number:
#             # If user_id is not provided, ask for it
#             dispatcher.utter_message(text="Please provide your Phone Number to proceed with the update.")
#             return []

#         payload = {
#             'username': username,
#             'email': email,
#             'age': age,
#             'phone_number': user_phone_number,
#             'income': income
#         }

#         api_url = f"http://127.0.0.1:8000/v1/user/{user_phone_number}"
#         response = requests.put(api_url, json=payload)

#         if response.status_code == 200:
#             dispatcher.utter_message(text="Your details have been successfully updated.")
#         else:
#             dispatcher.utter_message(text="There was an error updating your details. Please try again.")
#         # # Prepare the payload with user_id
#         # payload = {'phone_number': user_phone_number}
#         # message = ("Update Form, Please can tell your id")
#         # dispatcher.utter_message(text=message)
#         return []


class ActionUpdateUser(Action):
    def name(self) -> Text:
        return "action_update_user"
    
    def run(self,
            dispatcher:CollectingDispatcher,
            tracker:Tracker,
            domain: Dict[Text,Any]) -> List[Dict[Text,Any]]:
        
        phone_number = tracker.get_slot('phone_number')
        print(f"phone_number: {phone_number}")

        if phone_number:

            message = (
                "Please, tell me which field you want to update"
            )
            dispatcher.utter_message(text=message)

            return []

# class ActionFieldUpdateEmail(Action):
#     def name(self) -> Text:
#         return "action_field_update_email"
    
#     def run(self,
#             dispatcher:CollectingDispatcher,
#             tracker: Tracker,
#             domian:Dict[Text,Any]) -> List[Dict[Text, Any]]:
        
#         phone_number = tracker.get_slot('phone_number')
#         print(f"phone_number: {phone_number}")

#         if phone_number:

#             # name = tracker.get_slot('name')
#             # print(f"name: {name}")
#             email = tracker.get_slot("email")
#             print(f"email: {email}")
#             # age = tracker.get_slot("age")
#             # print(f"age: {age}")
#             # income = tracker.get_slot("income")
#             # print(f"income: {income}")
#             # message = (
#             #     "Please, tell me which field you want to update"
#             # )
#             # dispatcher.utter_message(text=message)
            
#             data_input = tracker.latest_message.get('text').lower()
#             print(f"data_input: {data_input}")
#             if data_input == "email":
#                 message = (f"Your mail is {email} \n \n Please Enter your new email")
#                 dispatcher.utter_message(text=message)
#                 empty_gmail = SlotSet("email",None)
#                 print(f"empty_gmail: {empty_gmail}")
#                 return [empty_gmail]
#             if tracker.get_slot('email') is None:
#                 new_email = tracker.latest_message.get('text').strip().lower()
#                 dispatcher.utter_message(text=f"Your email has been updated \n *Email*: {new_email}.")
#                 return [SlotSet("email", new_email)]


class ActionUpdateEmail(Action):
    def name(self) -> str:
        return "action_update_email"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> List[Dict[Text,Any]]:
        email = tracker.get_slot("email")
        dispatcher.utter_message(text=f"Your 📧 *email*: *{email}* \n \n Please provide the new email address:")
        return [SlotSet("email", None)]  # Clear the current email slot value


class ActionSetEmailForm(Action):
    def name(self) -> str:
        return "action_set_email_form"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> list:

        phone_number = tracker.get_slot("phone_number")
        print(f"Action set phone number: {phone_number}")
        if phone_number:
            new_email = tracker.latest_message.get('text').strip().lower()
            # get_email = tracker.get_slot('email').strip().lower()
            email = re.sub(r'\s+', '', new_email)
            print(f"This is email: {email}")
            if "@" in email and "." in email and len(email) > 7:
                dispatcher.utter_message(text=f"Your updated 📧 *email*: {new_email} \n \n  Do you want to update another field?")
                return {"email": email}
            else:
                dispatcher.utter_message(text="Please enter a valid email address.")
                return {"email": None}
            
    # def validate_email(self,
    #                 slot_value:Any,
    #                 dispatcher:CollectingDispatcher,
    #                 tracker: Tracker,
    #                 domain: Dict[Text,Any]) -> List[Dict[Text, Any]]:
    

    # get_email = tracker.get_slot('email').strip().lower()
    # email = re.sub(r'\s+', '', get_email)
    # print(f"This is email: {email}")
    # if "@" in email and "." in email and len(email) > 7:
    #     dispatcher.utter_message(text="Thanks! Now, could you please provide your age?")
    #     return {"email": email}
    # else:
    #     dispatcher.utter_message(text="Please enter a valid email address.")
    #     return {"email": None}

            

class ActionSubmitSetEmailForm(Action):
    def name(self) -> Text:
        return "action_submit_set_email_form"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> list:
        email  = tracker.get_slot("email")
        if email is not None:
            dispatcher.messages(text=f"Your Updated Email is {email}")
            return []
        else:
            dispatcher.messages(text=f"Can not Find Email: {email}")
            return []





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


class ActionSubmitUserDetailsForm(Action):
    def name(self) -> Text:
        return "action_submit_user_details_form"
    
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
            dispatcher.utter_message(text=f"User Form submitted successfully! ID: {result['id']}")
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


    def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_data = fetch_all_user_data()
        buttons = [
                {"title": "Main Menu", "payload": '/select_menu_item'}
            ]
        max_message_length = 1500
        if user_data:
            # buttons = [
            #     {"title": "Main Menu", "payload": '/select_menu_item'}
            #     ]
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


