import logging
from sanic import Blueprint, response
from sanic.request import Request
from sanic.response import HTTPResponse
from typing import Dict, Text, Any, Callable, Awaitable, Optional, TYPE_CHECKING

from rasa.core.channels.channel import InputChannel
from rasa.core.channels.channel import UserMessage, OutputChannel
import json

from heyoo import WhatsApp
import os
from dotenv import load_dotenv
load_dotenv()
import ast
from typing import (Text,List,Dict,Any,Optional,Callable,Awaitable)
# from logging_utils import # logger
logging.basicConfig(level=logging.INFO, format='%(message)s')


class WhatsAppOutput(WhatsApp, OutputChannel):
    """Output channel for WhatsApp Cloud API"""

    @classmethod
    def name(cls) -> Text:
        return "whatsapp"

    # def __init__(self,auth_token: Optional[Text],phone_number_id: Optional[Text],) -> None:
    #     super().__init__(auth_token, phone_number_id=phone_number_id)
    #     print(auth_token)
    #     self.client = WhatsApp(auth_token = self.auth_token, phone_number_id=self.phone_number_id)
    
    def __init__(self, auth_token: Optional[Text], phone_number_id: Optional[Text]) -> None:
        # Call the __init__ method of the parent class (WhatsApp)
        super().__init__(auth_token, phone_number_id=phone_number_id)
        # Now you can access auth_token and phone_number_id in the instance of WhatsAppOutput
        auth_token = os.getenv("WHATSAPP_ACCESS_TOKEN")
        phone_number_id = os.getenv("PHONE_NUMBER_ID")
        # auth_token = "EAAKoR0iQEzoBOws0AeBltNpMm9BPPHBazJ6wPpD9ebAa529TyqZBUz1ynyv1Y9d8nhBBXgbotOVqSMVZCMShVii2ZCHo61C0ljINASi3ZC7kZBFZBWQlGvkz4q1BxagbBnGeILRgxh7CHa0EfMUA61O6QCydvURPstZB4lUnfKK95TCv2MKvyLtj8YgSx50ZAA5r9jNLnq7uS1UpTAqCzG7ZCHjczxkymzmI4zZCcah6rgIHIj"
        # phone_number_id = "119229507784149"
        # phone_number_id = "163566040184368"
        self.client = WhatsApp(auth_token, phone_number_id)
        # self.client = WhatsApp(auth_token, phone_number_id=self.phone_number_id)
        # print(auth_token)

    async def send_text_message(
        self, recipient_id: Text, text: Text, **kwargs: Any
    ) -> None:
        """Sends text message"""
        logging.info(f"send message text: {text} receipient_id: {recipient_id}")
        # # logger(level="INFO", message=f"send message text: {text} receipient_id: {recipient_id}")
        
        # auth_token = "EAAOWp4YWFukBOZCuhOTYI30jAniCIVP1XbdYlZChuO7KbYlJqXA5Xq8mpDbnWNmVSY0o2hqFC7Xea8Gc0Ii9Q11s3nQp0IJUqBl2njIZCRneSqjMA4pux0TKzWKj2ZBeDMaZA1KjNZCkzqJFe0JFrPJSZAFZBesl5oyc9d3RwdR5QTK4XirWsNUsRHC0gTxpumk0Vv0IeYQTcnNOPMHiKy6y1fZBepsvXQjyvk70QLDSny4wHt3TvZBZAzw"
        # phone_number_id = "197738180088319"
        
        # auth_token = "EAAKoR0iQEzoBOws0AeBltNpMm9BPPHBazJ6wPpD9ebAa529TyqZBUz1ynyv1Y9d8nhBBXgbotOVqSMVZCMShVii2ZCHo61C0ljINASi3ZC7kZBFZBWQlGvkz4q1BxagbBnGeILRgxh7CHa0EfMUA61O6QCydvURPstZB4lUnfKK95TCv2MKvyLtj8YgSx50ZAA5r9jNLnq7uS1UpTAqCzG7ZCHjczxkymzmI4zZCcah6rgIHIj"
        # phone_number_id = "119229507784149"
        auth_token = os.getenv("WHATSAPP_ACCESS_TOKEN")
        phone_number_id = os.getenv("PHONE_NUMBER_ID")
        # phone_number_id = "163566040184368"
        
        self.client = WhatsApp(auth_token, phone_number_id)
        # print(auth_token)
        # print(phone_number_id)
        
        for message_part in text.strip().split("\n\n"):
            print(f"Message part : {message_part}")
            # logger(level="INFO", message=f"message part: {message_part}")
            logging.info(f"message part: {message_part}")
            # self.send_message(message_part, recipient_id=recipient_id, preview_url=False)
            self.client.send_message(message_part, recipient_id=recipient_id)

    # async def send_text_with_buttons(
    #     self,
    #     recipient_id: Text,
    #     text: Text,
    #     buttons: List[Dict[Text, Any]],
    #     **kwargs: Any,
    # ) -> None:
    #     """Sends text with buttons"""
    #     buttons_list = []
    #     print(f"in send button part : {buttons}")
    #     for button in buttons:
    #         buttons_list.append({
    #                     "type": "reply",
    #                     "reply": {
    #                         "id": button.get("payload"),
    #                         "title": button.get("title")
    #                     }
    #                 })
    #     button_dict = {"type": "button", "body": {
    #             "text": text},
    #             "action": {
    #                 "buttons": buttons_list
    #             }
    #         }
    #     self.send_reply_button(button=button_dict, recipient_id=recipient_id)
    
    # async def send_text_with_buttons(
    #     self,
    #     recipient_id: Text,
    #     text: Text,
    #     buttons: List[Dict[Text, Any]],
    #     **kwargs: Any,
    # ) -> None:
        
    #     buttons_sections_list = []
    #     rows_list = []
    #     print(f"in send list button part : {buttons}")
    #     for button in buttons:
    #         rows_list.append({
    #                         "id": button.get("payload"),
    #                         "title": button.get("title"),
    #                         "description": ""
    #                     })
            
    #     buttons_sections_list.append({
    #         "title": "Binary...",
    #         "rows": rows_list}) 
        
    #     list_dict = {
    #         "type": "list",
    #     "header": {
    #         "type": "text",
    #         "text": "Binary_Semantics"
    #             },
    #     "body": {
    #         "text": text
    #             },
    #     "footer": {
    #         "text": ""
    #             },
    #     "action": {
    #         "button": "Welcome",
    #         "sections" : buttons_sections_list 
    #         } 
    #     }
    #     self.client.send_list_with_button(lists=list_dict, recipient_id=recipient_id)
    
    # async def send_text_with_buttons(
    #     self,
    #     recipient_id: Text,
    #     text: Text,
    #     buttons: List[Dict[Text, Any]],
    #     **kwargs: Any,
    # ) -> None:
    #     buttons_sections_list = []
    #     rows_list = []
    #     print(f"in send list button part : {buttons}")
    #     for button in buttons:
    #         rows_list.append({
    #                         "id": button.get("payload"),
    #                         "title": button.get("title"),
    #                         "description": "hello1234"
    #                     })
            
    #     buttons_sections_list.append({
    #         "title": "Binary...",
    #         "rows": rows_list}) 
        
    #     list_dict = {
    #         "type": "list",
    #         "header": "Binary Semantics ltd",
    #         "body": text,
    #         "footer":"",
    #         "action": {
    #             "button": "Welcome",
    #             "sections" : buttons_sections_list 
    #             } 
    #         }
    #     self.send_button(button=list_dict, recipient_id=recipient_id)

    async def send_custom_json(
        self, recipient_id: Text, json_message: Dict[Text, Any], **kwargs: Any
    ) -> None:
        """Sends custome json"""
        # location_data = json.dumps(json_message)

        if json_message["type"] == "document":
            logging.info(f"send document from the whatsapp: {json_message}")
            # logger(level="INFO", message=f"send document from the whatsapp: {json_message}")
            document_url = json_message["document_info"]["document_url"]
            document_name = json_message["document_info"]["document_name"]
            document_caption = json_message["document_info"]["caption"]
            self.send_document(document_url,recipient_id,caption=document_caption, link=True, filename=document_name)

        # if json_message["type"] == "location":
        #     print(f"in send location message part : {json_message}")
        #     lat = json_message["location_info"]["latitude"]
        #     long = json_message["location_info"]["longitude"]
        #     name = json_message["location_info"]["name"]
        #     address = json_message["location_info"]["address"]
        #     self.send_location(lat,long,name,address,recipient_id)
            
        # elif json_message["type"] == "template":  
        #     print(f"in send template part : {json_message}")
        #     template = json_message["template_info"]["name"]  
        #     components = json_message["template_info"]["components"] 
        #     lang = json_message["template_info"]["language"]["code"]
        #     self.send_template(template, recipient_id, components, lang)
            
        # elif json_message["type"] == "contacts":
        #     contacts = json_message["contact_info"]
        #     self.send_contacts(contacts, recipient_id)
            
        else:
            logging.info(f"unknown type data received: {json_message['type']}")
            # logger(level="INFO", message=f"unknown type data received: {json_message['type']}")
        

    # async def send_text_with_buttons(
    #     self,
    #     recipient_id: Text,
    #     text: Text,
    #     buttons: List[Dict[Text, Any]],
    #     **kwargs: Any,
    # ) -> None:
    #     buttons_sections_list = []
    #     rows_list = []
    #     button_description = {
    #         "🔄 Main Menu" : "Go to main menu",
    #         "🔄 Renew Policy": "Renew your policy now",
    #         "🆕 New Policy": "Buy a new policy",
    #         "📋 Claims Related": "Register or track your claim",
    #         "⬇️ Download Policy": "Download your policy",
    #         "🛠️ Nearby Workshop": "Search for nearby workshop",
    #         "🚨 Emergency Support": "Emergency Support"
    #     }
    #     # print(f"in send list button part : {buttons}")
    #     for button in buttons:
    #         rows_list.append({
    #                         "id": button.get("payload"),
    #                         "title": button.get("title"),
    #                         "description": button_description.get(button.get("title"), "")
    #                     })
    #     print("row list: ",rows_list)
    #     buttons_sections_list.append({
    #         "title": "Binary...",
    #         "rows": rows_list}) 
        
    #     list_dict = {
    #         "type": "list",
    #         "header": "Binary Semantics ltd",
    #         "body": text,
    #         "footer":"",
    #         "action": {
    #             "button": "Show Options",
    #             "sections" : buttons_sections_list 
    #             } 
    #         }
    #     self.send_button(button=list_dict, recipient_id=recipient_id)

    async def send_text_with_buttons(
        self,
        recipient_id: Text,
        text: Text,
        buttons: List[Dict[Text, Any]],
        **kwargs: Any,
    ) -> None:
        buttons_sections_list = []
        rows_list = []
        button_description = {
            "🔄 Renew Policy": "Renew your policy now",
            "🆕 New Policy": "Buy a new policy",
            "📋 Claims Related": "Register or track your claim",
            "⬇️ Download Policy Copy": "Download your policy",
            "🛠️ Nearby Workshop": "Search for nearby workshop",
            "🚨 Emergency Support": "Emergency Support"
        }
        # print(f"in send list button part : {buttons}")
        logging.info(f"display button from the whatsapp: {buttons}")
        # logger(level="INFO",message=f"display button from the whatsapp: {buttons}")
        titles = [item['title'] for item in buttons]
        static_keys = list(button_description.keys())
        all_present = all(k in static_keys for k in titles)
        if all_present:
            for button in buttons:
                # description = button.get("description")
                rows_list.append({
                                "id": button.get("payload"),
                                "title": button.get("title"),
                                "description": button_description.get(button.get("title"), "")
                                # "description": description
                            })
        else:
            for button in buttons:
                description = button.get("description")
                rows_list.append({
                                "id": button.get("payload"),
                                "title": button.get("title"),
                                # "description": button_description.get(button.get("title"), "")
                                "description": description
                            })
        
        check_title = rows_list[0]
        logging.info(f"value of title: {check_title}")
        logging.info(f"value of title id: {check_title['id']}")
        
        # logging.info(f"value of button_list_name: {button_list_name}")
        # logger(level="INFO", message=f"value of title: {check_title} id: {check_title['id']} button_list_name: {button_list_name}")

        # button_list_name = "Main Menu"
        if ("policy_selected" in check_title["id"] or "policyno" in check_title["id"] or "renewal_policyno" in check_title["id"]):
            if "hindi" in check_title["id"]:
                button_list_name = "पॉलिसी देखें"
            elif "english" in check_title["id"]:
                button_list_name = "Show Policy"
        elif "renewal_policy" in check_title["id"]:
            if "hindi" in check_title["id"]:
                button_list_name = "मेन मेन्यू"
            elif "english" in check_title["id"]:
                button_list_name = "Main Menu"
        elif ("selected_insurance" in check_title["id"]):
            if "hindi" in check_title["id"]:
                button_list_name = "क्वोट्स देखें"
            elif "english" in check_title["id"]:
                button_list_name = "Show Quotes"
        elif ("selected_addons" in check_title["id"]):
            if "hindi" in check_title["id"]:
                button_list_name = "ऐड-ऑन"
            elif "english" in check_title["id"]:
                button_list_name = "Add Ons"
        elif ("make_payment" in check_title["id"]):
            if "hindi" in check_title["id"]:
                button_list_name = "भुगतान करें"
            elif "english" in check_title["id"]:
                button_list_name = "Make Payment"
        
        # logging.info(f"button list name: {button_list_name}")
        # logger(level="INFO", message=f"button list name: {button_list_name}")


                
        # print(rows_list)
        buttons_sections_list.append({
            "title": "Binary...",
            "rows": rows_list})
        if (len(buttons) >4 or 
            len([item["payload"] for item in buttons if "policy_details" in item["payload"]])>0 or 
            len([item["payload"] for item in buttons if "packageId" in item["payload"]])>0 or
            len([item["payload"] for item in buttons if "selected_policy_number" in item["payload"]])>0 or
            len([item["payload"] for item in buttons if "policyno" in item["payload"]])>0  or
            len([item["payload"] for item in buttons if "renewal_policyno" in item["payload"]])>0 or
            len([item["payload"] for item in buttons if "payment_selected_option" in item["payload"]])>0 
        ):
            # titles = [item['title'] for item in buttons]
            # static_keys = list(button_description.keys())
            # all_present = all(k in static_keys for k in titles)
            # if all_present:
            #     for button in buttons:
            #         # description = button.get("description")
            #         rows_list.append({
            #                         "id": button.get("payload"),
            #                         "title": button.get("title"),
            #                         "description": button_description.get(button.get("title"), "")
            #                         # "description": description
            #                     })
            # else:
            #     for button in buttons:
            #         description = button.get("description")
            #         rows_list.append({
            #                         "id": button.get("payload"),
            #                         "title": button.get("title"),
            #                         # "description": button_description.get(button.get("title"), "")
            #                         "description": description
            #                     })
            
            # check_title = rows_list[0]
            # logging.info(f"value of title: {check_title}")
            # logging.info(f"value of title id: {check_title['id']}")
            # button_list_name = "Main Menu"
            # logging.info(f"value of button_list_name: {button_list_name}")
            # # logger(level="INFO", message=f"value of title: {check_title} id: {check_title['id']} button_list_name: {button_list_name}")

            # # button_list_name = "Main Menu"
            # if ("policy_selected" in check_title["id"] or "policyno" in check_title["id"] or "renewal_policyno" in check_title["id"]):
            #     if "hindi" in check_title["id"]:
            #         button_list_name = "पॉलिसी देखें"
            #     elif "english" in check_title["id"]:
            #         button_list_name = "Show Policy"
            # elif "renewal_policy" in check_title["id"]:
            #     if "hindi" in check_title["id"]:
            #         button_list_name = "मेन मेन्यू"
            #     elif "english" in check_title["id"]:
            #         button_list_name = "Main Menu"
            # elif ("selected_insurance" in check_title["id"]):
            #     if "hindi" in check_title["id"]:
            #         button_list_name = "क्वोट्स देखें"
            #     elif "english" in check_title["id"]:
            #         button_list_name = "Show Quotes"
            # elif ("selected_addons" in check_title["id"]):
            #     if "hindi" in check_title["id"]:
            #         button_list_name = "ऐड-ऑन"
            #     elif "english" in check_title["id"]:
            #         button_list_name = "Add Ons"
            # elif ("make_payment" in check_title["id"]):
            #     if "hindi" in check_title["id"]:
            #         button_list_name = "भुगतान करें"
            #     elif "english" in check_title["id"]:
            #         button_list_name = "Make Payment"
            
            # logging.info(f"button list name: {button_list_name}")
            # # logger(level="INFO", message=f"button list name: {button_list_name}")


                   
            # # print(rows_list)
            # buttons_sections_list.append({
            #     "title": "Binary...",
            #     "rows": rows_list})
            button_list_name = "Main Menu"
            list_dict = {
                "type": "list",
                "header": "",
                "body": text,
                "footer":"",
                "action": {
                    "button": button_list_name,
                    "sections" : buttons_sections_list
                    }
                }
            self.send_button(button=list_dict, recipient_id=recipient_id)
        elif(len(buttons) ==4 or
            len([item["payload"] for item in buttons if "policy_details" in item["payload"]])>0 or 
            len([item["payload"] for item in buttons if "packageId" in item["payload"]])>0 or
            len([item["payload"] for item in buttons if "selected_policy_number" in item["payload"]])>0 or
            len([item["payload"] for item in buttons if "policyno" in item["payload"]])>0  or
            len([item["payload"] for item in buttons if "renewal_policyno" in item["payload"]])>0 or
            len([item["payload"] for item in buttons if "payment_selected_option" in item["payload"]])>0 
        ):

            button_list_name = "Update Fields"
            list_dict = {
                "type": "list",
                "header": "",
                "body": text,
                "footer":"",
                "action": {
                    "button": button_list_name,
                    "sections" : buttons_sections_list
                    }
                }
            self.send_button(button=list_dict, recipient_id=recipient_id)
        else:
            """Sends text with buttons"""
            buttons_list = []
            logging.info(f"in send button part : {buttons}")
            # logger(level="INFO", message=f"in send button part : {buttons}")
            for button in buttons:
                buttons_list.append({
                            "type": "reply",
                            "reply": {
                                "id": button.get("payload"),
                                "title": button.get("title")
                            }
                        })
            button_dict = {"type": "button", "body": {
                    "text": text},
                    "action": {
                        "buttons": buttons_list
                    }
                }
            self.send_reply_button(button=button_dict, recipient_id=recipient_id)
           
    #future modification -1
    async def send_image_url(
        self, recipient_id: Text, image: Text, **kwargs: Any
    ) -> None:
        """Sends an image."""
        logging.info(f"in send image part : {image}")
        # logger(level="INFO", message=f"in send image part : {image}")
        self.send_image(image, recipient_id=recipient_id)
    

class WhatsAppInput(InputChannel):
    """WhatsApp Cloud API input channel"""

    user_mobile = None 

    @classmethod
    def name(cls) -> Text:
        return "whatsapp"

    @classmethod
    def from_credentials(cls, credentials: Optional[Dict[Text, Any]]) -> InputChannel:
        if not credentials:
            cls.raise_missing_credentials_exception()

        return cls(
            credentials.get("auth_token"),
            credentials.get("phone_number_id"),
            credentials.get("verify_token")
        )

    def __init__(
        self,
        auth_token: Optional[Text],
        phone_number_id: Optional[Text],
        verify_token: Optional[Text],
        debug_mode: bool = True,
    ) -> None:
        # self.auth_token = auth_token
        # self.phone_number_id = phone_number_id
        # self.verify_token = verify_token
        # self.debug_mode = debug_mode
        
        # auth_token = "EAAOWp4YWFukBOZCuhOTYI30jAniCIVP1XbdYlZChuO7KbYlJqXA5Xq8mpDbnWNmVSY0o2hqFC7Xea8Gc0Ii9Q11s3nQp0IJUqBl2njIZCRneSqjMA4pux0TKzWKj2ZBeDMaZA1KjNZCkzqJFe0JFrPJSZAFZBesl5oyc9d3RwdR5QTK4XirWsNUsRHC0gTxpumk0Vv0IeYQTcnNOPMHiKy6y1fZBepsvXQjyvk70QLDSny4wHt3TvZBZAzw"
        # phone_number_id = "197738180088319"
        
        # auth_token = "EAAKoR0iQEzoBOws0AeBltNpMm9BPPHBazJ6wPpD9ebAa529TyqZBUz1ynyv1Y9d8nhBBXgbotOVqSMVZCMShVii2ZCHo61C0ljINASi3ZC7kZBFZBWQlGvkz4q1BxagbBnGeILRgxh7CHa0EfMUA61O6QCydvURPstZB4lUnfKK95TCv2MKvyLtj8YgSx50ZAA5r9jNLnq7uS1UpTAqCzG7ZCHjczxkymzmI4zZCcah6rgIHIj"
        # phone_number_id = "119229507784149"
        auth_token = os.getenv("WHATSAPP_ACCESS_TOKEN")
        phone_number_id = os.getenv("PHONE_NUMBER_ID")
        # phone_number_id = "163566040184368"
        verify_token =  "whatsapp"
        
        self.auth_token = auth_token
        self.phone_number_id = phone_number_id
        self.verify_token = verify_token
        self.debug_mode = debug_mode
        
        logging.info(f"auth token in input class : {auth_token}")
        logging.info(f"phone number id in input class : {phone_number_id}")
        logging.info(f"verify token in input class : {self.verify_token}")
        # logger(level="INFO", message=f"whatsapp auth token: {auth_token} phone_number_id: {phone_number_id} verify_token: {verify_token}")
        self.client = WhatsApp(self.auth_token, phone_number_id=self.phone_number_id)
        
    # def get_message(self, data):
    #     message_type = self.client.get_message_type(data)
    #     if message_type == "interactive":
    #         response = self.client.get_interactive_response(data)
            
    #         if response.get("type") == "button_reply":
    #             return response.get("button_reply").get("id")
    #     return self.client.get_message(data)
    
    def get_message(self, data):
        message_type = self.client.get_message_type(data)
        logging.info(f"message type is: {message_type}")
        # logger(level="INFO", message=f"message type is: {message_type}")
        
        if message_type == "text":
            logging.info(f"text data is : {self.client.get_message(data)}")
            return self.client.get_message(data)
        
        elif message_type == "image":
            image_data = self.client.get_image(data)
            logging.info(f"image data is : {image_data}")
            # logger(level="INFO", message=f"image data is : {image_data}")
            if image_data:
                image_id = image_data['id']
                logging.info(f"user image id: {image_id}")
                # logger(level="INFO", message=f"user image id: {image_id}")
            return f"Image is {image_id}"
            # image_data = self.client.get_image(data)
            # return "Received....!!", image_data
            
        elif message_type == "document":
            doc_data = self.client.get_document(data)
            logging.info(f"user document is : {doc_data}")
            # logger(level="INFO", message=f"user document is : {doc_data}")
            if doc_data:
                doc_id = doc_data['id']
                logging.info(f"user document id: {doc_id}")
                # logger(level="INFO", message=f"user document is : {doc_data}")
            return f"document is {doc_id}"
        
        elif message_type == "video":
            video_data = self.client.get_video(data)
            logging.info(f"user video data is : {video_data}")
            # logger(level="INFO", message=f"user video data is : {video_data}")
            if video_data:
                video_id = video_data['id']
                logging.info(f"user video id: {video_id}")
                # logger(level="INFO", message=f"user video data is : {video_data}")
            return f"video id is {video_id}"
        
        elif message_type == "audio":
            audio_data = self.client.get_audio(data)
            logging.info(f"user audio data is : {audio_data}")
            # logger(level="INFO", message=f"user audio data is : {audio_data}")
            if audio_data:
                audio_id = audio_data['id']
                logging.info(f"user audio id: {audio_id}")
                # logger(level="INFO", message=f"user audio data is : {audio_data}")
            return f"audio id is {audio_id}"
        
        elif message_type == "location":
            location = self.client.get_location(data)
            if location:
                latitude = location['latitude']
                longitude = location['longitude']
            logging.info(f"user location: {location}")
            # logger(level="INFO", message=f"user location: {location}")
            return f"Location of accident is Received with Latitude {latitude} and Longitude is {longitude}"
        
        elif message_type == "interactive":
            response = self.client.get_interactive_response(data)
            logging.info(f"Interactive response is : {response}")
            # logger(level="INFO", message=f"interactive response is: {response}")
            response_type = response.get("type")
            logging.info(f"response type in interactive: {response_type}")
            # logger(level="INFO", message=f"response type in interactive: {response_type}")
            
            if response.get("type") == "button_reply":
                return response.get("button_reply").get("id")
            
            # {'type': 'button_reply', 'button_reply': {'id': '/schedule_meeting', 'title': 'Book Appointment'}}
            # {'type': 'list_reply', 'list_reply': {'id': 'claim', 'title': 'Immediate claim'}}
            # {'type': 'list_reply', 'list_reply': {'id': '/claim', 'title': 'Immediate claim', 'description': 'Immediate claim for damage vehicles'}}
            #added code for list response
            elif response.get("type") == "list_reply":
                return response.get("list_reply").get("id")
            

            elif response.get("type") == "nfm_reply":
                reply_type = response.get("nfm_reply")
                logging.info(f"type nfm reply in interactive response: {reply_type}")
                # logger(level="INFO", message=f"type nfm replay in interactive response: {reply_type}")

                communication_type, value = extract_communication_types(str(reply_type))
                logging.info(f"value of extracted communication type: {communication_type} value: {value}")
                # logger(level="INFO", message=f"value of extracted communication type: {communication_type} value: {value}")

                if communication_type and value:

                    if communication_type == "add_ons":
                        # add_ons_list = extract_communication_types(str(reply_type))
                        logging.info(f"extracted addons list type: {type(value)} value: {value}")
                        if value:
                            add_on_ids = ""
                            for i in value:
                                add_on_ids = add_on_ids + i + "," 

                            logging.info(f"extracted value of add on ids from the whatsapp flows: {add_on_ids}")
                            # logger(level="INFO", message=f"extracted value of add on ids from the whatsapp flows: {add_on_ids}")
                            
                            if len(add_on_ids) > 0:
                                extracted_id = f"selected add on quotes values {add_on_ids[:-1]} from the whatsapp response"
                                logging.info(f"add on ids message for rasa: {extracted_id}")
                                # logger(level="INFO", message=f"add on ids message for rasa: {extracted_id}")
                                return extracted_id
                    
                    elif communication_type == "download_policy":
                        extracted_data = f"policy affirm policy extraction using regex for DOWNLOAD_{value}_POLICY slot set at the end slot has been going to set for this"
                        logging.info(f"extracted_data: {extracted_data}")
                        # logger(level="INFO", message=f"extracted_data: {extracted_data}")
                        return extracted_data
                    

                    elif communication_type == "claim_status":
                        extracted_data = f"claim status policy is selected by the user as CLAIM_RELATED_{value}_POLICY and it will return the status of the claim and this process will follow subsequently."
                        logging.info(f"extracted_data: {extracted_data}")
                        # logger(level="INFO", message=f"extracted_data: {extracted_data}")
                        return extracted_data
                    

                    elif communication_type == "claim_intimation":
                        extracted_data = f"claim status policy is selected by the user as CLAIM_RELATED_{value}_POLICY and it will return the status of the claim and this process will follow subsequently."
                        logging.info(f"extracted_data: {extracted_data}")
                        # logger(level="INFO", message=f"extracted_data: {extracted_data}")
                        return extracted_data
                
                    elif communication_type == "renew_policy":
                        extracted_data = f"found multiple policies. Extracted one policy for renewal that is RENEWAL_{value}_POLICY and its going for renew my policy as per rules and regulations"
                        logging.info(f"extracted_data: {extracted_data}")
                        # logger(level="INFO", message=f"extracted_data: {extracted_data}")
                        return extracted_data
                    
                    elif communication_type == "premium_quotes":
                        extracted_data = f"selecting premium quotes for the vehical {value} and extract product id, proposal id and ic code which is helpful to extract the data for add ons"
                        logging.info(f"extracted_data: {extracted_data}")
                        # logger(level="INFO", message=f"extracted_data: {extracted_data}")
                        return extracted_data
                        
                # return response.get("nfm_replay").get("id")
                # return response.get("list_reply").get("description")
            
        return self.client.get_message(data)
        # return "Unsupported message type"
    
    def blueprint(
        self, on_new_message: Callable[[UserMessage], Awaitable[Any]]
    ) -> Blueprint:
        whatsapp_webhook = Blueprint("whatsapp_webhook", __name__)

        @whatsapp_webhook.route("/", methods=["GET"])
        async def health(_: Request) -> HTTPResponse:
            return response.json({"status": "ok"})

        # @whatsapp_webhook.route("/webhook/{verification_token}", methods=["POST"])
        # async def verify_token(verification_token: str) -> HTTPResponse:
        #     # verification_token = request.args.get("hub.verify_token")
        #     logging.info(f"received token for verification : {verification_token}")
        #     # print(request.json.get("hub.verify_token"))
        #     logging.info(f"set token for verification : {self.verify_token}")
        #     # logging.info(request.args.get("hub.verify_token") == self.verify_token)
        #     # logging.info(request.args.get("hub.verify_token") == self.verify_token)
        #     # if request.args.get("hub.verify_token") == self.verify_token:
        #     #    return response.text(request.args.get("hub.challenge"))
        #     # logging.error("webhook verification has been failed")
        #     # logger(level='ERROR', message=f"webhook verification has been failed")
        #     return "Invalid verification token"
        
        @whatsapp_webhook.route("/webhook", methods=["GET"])
        async def verify_token(request: Request) -> HTTPResponse:
            logging.info(f"request for verification : {request.json}")
            verification_token = request.args.get("hub.verify_token")
            logging.info(f"received token for verification : {verification_token}")
            # print(request.json.get("hub.verify_token"))
            logging.info(self.verify_token)
            logging.info(request.args.get("hub.verify_token") == self.verify_token)
            if request.args.get("hub.verify_token") == self.verify_token:
               return response.text(request.args.get("hub.challenge"))
            logging.error("webhook verification has been failed")
            # logger(level='ERROR', message=f"webhook verification has been failed")
            return "Invalid verification token"



        @whatsapp_webhook.route("/webhook", methods=["POST"])
        async def message(request: Request) -> HTTPResponse:
            logging.info(f"whatsapp response outside: {request.json}")
            sender = self.client.get_mobile(request.json)

            if sender:
                global user_mobile
                user_mobile = sender
                logging.info(f"user mobile no: {sender}")
            
            logging.info(f"whatsapp webhook request: {request.json}")
            # logger(level='INFO', message=f"whatsapp webhook request: {request.json}")
            # text = self.client.get_message(request.json)  # TODO This will not work for image caption and buttons
            
            text = self.get_message(request.json)
            # text, image_data = self.get_message(request.json) #up
            logging.info(f"whatsapp user message text: {text}")
            # logger(level="INFO", message=f"whatsapp user message text: {text}")
            
            metadata = self.get_metadata(request.json)
            logging.info(f"whatsapp message metadata: {text}")
            # logger(level="INFO", message=f"whatsapp message metadata: {text}")
            out_channel = self.get_output_channel()
            # print(f"out channel: {out_channel}")
            if sender is not None and text is not None:
                logging.info(f"inside whatsapp response")
                # logger(level="INFO", message=f"inside whatsapp response")
                metadata = {"sender": sender}
                logging.info(f"updated whatsapp metadata for rasa: {metadata}")
                # logger(level="INFO", message=f"updated whatsapp metadata for rasa: {metadata}")
                # metadata = self.get_metadata(request)
                try:
                    logging.info("inside try block")
                    # logger(level="INFO", message=f"message are ready to send to rasa from whatsapp")
                    await on_new_message(
                        UserMessage(
                            text,
                            out_channel,
                            sender,
                            input_channel=self.name(),
                            metadata=metadata
                        )
                    )
                except Exception as e:
                    logging.error(f"exception when trying to handle whatsapp message: {e}")
                    # logger(level="ERROR",message=f"exception when trying to handle whatsapp message: {e}")
                    # logger.debug(e, exc_info=True)
                    if self.debug_mode:
                        raise
                    pass
            else:
                logging.info(f"sender id and text message is missing in message")
                # logger(level="INFO", message=f"sender id and text message is missing in message")

            return response.text("", status=204)

        return whatsapp_webhook

    def get_output_channel(self) -> OutputChannel:
        output_result = WhatsAppOutput(self.auth_token, self.phone_number_id)
        # print(f"output response: {output_result}")
        return output_result
        # return WhatsAppOutput(self.auth_token, self.phone_number_id)




def extract_communication_types(data_str):
    """
    Extracts the list of communication types from the given string.

    Args:
    data_str (str): Input string containing the communication types JSON.

    Returns:
    list: A list of communication types if found, otherwise an empty list.
    """
    try:
        import re
        logging.info(f"Input data string: {data_str}")
        # logger(level="INFO", message=f"Input data string: {data_str}")
        check_string = "communicationTypes"
        index = data_str.index(check_string)
        if data_str[index:index + len(check_string)] == check_string:
            data_str = data_str[index + len(check_string) + 2:]
            logging.info(f"String after 'communicationTypes': {data_str}")
            # logger(level="INFO", message=f"String after 'communicationTypes': {data_str}")

            if "download_policy_" in data_str:
                logging.info(f"Download policy in flows: {data_str}")
                # logger(level="INFO", message=f"Download policy in flows: {data_str}")
                
                # Extract the policy code using a regular expression
                match = re.search(r'download_policy_(\w+)', data_str)
                if match:
                    policy_code = match.group(1)
                    logging.info(f"Extracted Policy Code: {policy_code}")
                    return "download_policy", policy_code
                

            elif "claim_status_" in data_str:
                logging.info(f"Claim Status in flows: {data_str}")
                # logger(level="INFO", message=f"Claim Status in flows: {data_str}")
                
                # Extract the policy code using a regular expression
                match = re.search(r'claim_status_(\w+)', data_str)
                if match:
                    policy_code = match.group(1)
                    logging.info(f"Extracted Policy Code: {policy_code}")
                    return "claim_status", policy_code


            elif "claim_intimation_" in data_str:
                logging.info(f"Claim Intimation in flows: {data_str}")
                # logger(level="INFO", message=f"Claim Intimation in flows: {data_str}")
                
                # Extract the policy code using a regular expression
                match = re.search(r'claim_intimation_(\w+)', data_str)
                if match:
                    policy_code = match.group(1)
                    logging.info(f"Extracted Policy Code: {policy_code}")
                    return "claim_status", policy_code
                
            elif "renew_" in data_str:
                logging.info(f"Renew Policy in flows: {data_str}")
                # logger(level="INFO", message=f"Renew Policy in flows: {data_str}")
                
                # Extract the policy code using a regular expression
                match = re.search(r'renew_(\w+)', data_str)
                if match:
                    policy_code = match.group(1)
                    logging.info(f"Extracted Policy Code: {policy_code}")
                    return "renew_policy", policy_code
                
            elif "premium_" in data_str:
                logging.info(f"Premium Quotes in flows: {data_str}")
                # logger(level="INFO", message=f"Renew Policy in flows: {data_str}")
                
                # Extract the policy code using a regular expression
                match = re.search(r'premium_(\w+)', data_str)
                if match:
                    policy_code = match.group(1)
                    logging.info(f"Extracted Policy Code: {policy_code}")
                    return "premium_quotes", policy_code

                

            index_start = data_str.index("[")
            index_end = data_str.index("]")
            logging.info(f"Start index: {index_start}, End index: {index_end}")
            # logger(level="INFO", message=f"Start index: {index_start}, End index: {index_end}")

            list_str = data_str[index_start:index_end + 1]
            logging.info(f"Extracted list string: {list_str}")
            # logger(level="INFO", message=f"Extracted list string: {list_str}")

            communication_types = ast.literal_eval(list_str)
            logging.info(f"Extracted communication types: {communication_types}")
            # logger(level="INFO", message=f"Extracted communication types: {communication_types}")
            return "add_ons", communication_types
        else:
            logging.info(f"value is not matched with communication types: {data_str[index:index + len(check_string)]}")
            # logger(level="INFO", message=f"value is not matched with communication types: {data_str[index:index + len(check_string)]}")
            return None, None
    except Exception as e:
        logging.error(f"Error while extracting communication types: {e}")
        # logger(level="ERROR", message=f"Error while extracting communication types: {e}")
        return None, None
