from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction

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
                {"title": "Nearly Workshop", "payload": '/nearly workshop'},
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
