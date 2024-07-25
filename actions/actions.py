from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction
from rasa_sdk.types import DomainDict


class ActionGreetUser(Action):

    def name(self) -> Text:
        return "action_greet_user"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        message = ("""
            Hi Vivek,

            I am VISoF Buddy, Your WhatsApp Insurance Assistance.

            Your Hyundai Verna DL - 3CBU - 6767 Insurance Policy (Policy No: 3423223276548663)

            is valid till 28 Feb 2024.

            Let’s get started with your renewal, claims, or any other insurance-related support.

            Please select your language.
            """
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
            message = ("""
                Need help with renewal, claims or any other insurance-related support.

                Click on *Main Menu*
            """)
            buttons = [
                {"title": "Renew Policy", "payload": '/renew_policy'},
                {"title": "Claims Related", "payload": '/claims_related'},
                {"title": "Download Policy Copy", "payload": '/download_policy'},
                {"title": "Emergengy Support", "payload": '/emergency_support'},
                {"title": "Nearly Workshop", "payload": '/near_by_workshop'},
                {"title": "New Policy", "payload": '/new_policy'},
                {"title": "Health Policy", "payload": '/health_policy'}
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
                """
                Incase you need repair service enter pincode and share current location to connect nearest workshop.

                If you require any assistance, 

                Call - 1800XXXXXXXXX
                Missed call and get callback:
                9876543211
                
                """
            )
            dispatcher.utter_message(text=message)
            return [
                # FollowupAction("emergency_pincode_form")
            ]


class ActionNearByWorkshop(Action):
    def name(self) -> Text:
        return "action_near_by_workshop"
    def run(self,
            dispatcher: CollectingDispatcher,
            tracker:Tracker,
            domain:Dict[Text, Any]) -> List[Dict[Text, Any]]:
        message = ("""
            🙂We are happy to assist you.

            Please enter the Pincode or share your current location.
        """)

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
            message = ("""
                Looks like the location is invalid.

                Please enter the pincode or share your current location 
            """)
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
            message = ("""
                Great! We found 1 Garages near you. Given below are the details of workshops:

                Superon
                Tele No : 9876543211
                
                Safdarjang
                Tele No : 8765432123

                Click below link to view garages on map.

                https://dxa2.jcowk/oxwo=jcwojcown

                if you require any assistance, 

                Call - 1800XXXXXXXXX
                Missed call and get callback:
                9876543211   
            """)
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
            message = ("""
                Looks like the location is invalid.

                Please enter the pincode or share your current location 
            """)
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
            message = ("""
                Great! We found 1 Garages near you. Given below are the details of workshops:

                Superon
                Tele No : 9876543211
                
                Safdarjang
                Tele No : 8765432123

                Click below link to view garages on map.

                https://dxa2.jcowk/oxwo=jcwojcown

                if you require any assistance, 

                Call - 1800XXXXXXXXX
                Missed call and get callback:
                9876543211
            """)
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
        
        message = ("""
            You are now in the Health Policy section.
            Here, you will find information and updates on healthcare regulations, policies, and initiatives.
            Explore the latest developments to stay informed and make well-informed decisions about your health and wellness.
        """)
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
        

        email = tracker.get_slot('email').strip().lower()
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

        message = (f"""
            Details of the Form:                   

            Your name is {name}
            Your email is {email}
            Your age is {age}
            Your Phone Number is {phone_number}
            Your Income is {income}
        """)
        buttons = [
                {"title": "Main Menu", "payload": '/select_menu_item'}
            ]
        dispatcher.utter_message(text=message, buttons=buttons)
        
        return [
            SlotSet('name', None),
            SlotSet('email', None),
            SlotSet('age', None),
            SlotSet('phone_number', None),
            SlotSet('income', None)
        ]

