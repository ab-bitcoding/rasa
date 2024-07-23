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
        
            buttons = [
                {"title": "Renew Policy", "payload": '/renew_policy'},
                {"title": "Claims Related", "payload": '/claims_related'},
                {"title": "Download Policy Copy", "payload": '/download_policy'},
                {"title": "Emergengy Support", "payload": '/emergency_support'},
                {"title": "Nearly Workshop", "payload": '/near_by_workshop'},
                {"title": "New Policy", "payload": '/new_policy'},
            ]

            dispatcher.utter_message(buttons=buttons)

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
