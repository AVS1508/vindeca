# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from typing import Any, Text, Dict, List, Union

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction, REQUESTED_SLOT
from rasa_sdk.events import AllSlotsReset, ActiveLoop, SlotSet, EventType

# class FormCoronavirusAssessment(FormAction):
#     def __init__(self):
#         print('Created')

#     def name(self) -> Text:
#         return "form_coronavirus_assessment"

#     @staticmethod
#     def required_slots(tracker: Tracker) -> List[Text]:
#         return ["1_is_vaccinated", "2_vaccine_brand", "3_num_doses", "4_past_infection", "5_current_symptoms", "6_preexisting_conditions", "7_travel_interstate"]
    
#     def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
#         return {
#             "1_is_vaccinated": self.from_text(),
#             "2_vaccine_brand": self.from_text(),
#             "3_num_doses": self.from_text(),
#             "4_past_infection": self.from_text(),
#             "5_current_symptoms": self.from_text(),
#             "6_preexisting_conditions": self.from_text(),
#             "7_travel_interstate": self.from_text(),
#         }
    
#     def submit (self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
#         return []

class ActionResetSlots(Action):
    def name(self) -> Text:
        return "action_reset_slots"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text,Any]]:
        return [AllSlotsReset()]

class UtterCoronavirusAssessment(Action):
    def name(self) -> Text:
        return "explain_coronavirus_assessment"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text,Any]]:
        if tracker.slots.get("3_num_doses", None) == '2':
            dispatcher.utter_message("Your infection risk is LOW as you are fully vaccinated. We still recommend that you stay at home to avoid any chance of exposure to the Novel Coronavirus!")
        elif tracker.slots.get("3_num_doses", None) == '1':
            if not (tracker.slots.get("4_past_infection", None) == "true" or tracker.slots.get("5_current_symptoms", None) == "true" or tracker.slots.get("6_preexisting_conditions", None) == "true" or tracker.slots.get("7_travel_interstate", None) == "true"):
                dispatcher.utter_message("Your infection risk is LOW as you are partially vaccinated with no other adverse factors. We recommend that you stay at home to avoid any chance of exposure to the Novel Coronavirus, and receive your 2nd dose at the earliest!")
            else:
                dispatcher.utter_message("Your infection risk is MEDIUM as you are partially vaccinated with some adverse factor(s). We recommend that you stay at home to avoid any chance of exposure to the Novel Coronavirus, and receive your 2nd dose at the earliest!")
        elif tracker.slots.get("3_num_doses", None) == '0':
            if not (tracker.slots.get("4_past_infection", None) == "true" or tracker.slots.get("5_current_symptoms", None) == "true" or tracker.slots.get("6_preexisting_conditions", None) == "true" or tracker.slots.get("7_travel_interstate", None) == "true"):
                dispatcher.utter_message("Your infection risk is MEDIUM as you are not vaccinated but no other adverse factors. We strictly recommend that you stay at home to avoid any chance of exposure to the Novel Coronavirus, and get started with your vaccinations soon!")
            else:
                dispatcher.utter_message("Your infection risk is HIGH as you are not vaccinated and have other adverse factor(s). We strictly recommend that you stay at home to avoid any chance of exposure to the Novel Coronavirus, and get started with your vaccinations soon!")
        else:
            dispatcher.utter_message("I am still learning how to process this data to estimate your risk levels! Till then, kindly maintain social distancing in public and wear masks extensively in order to protect everyone.")
        return []

class ValidateForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_form_coronavirus_assessment"
    
    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[EventType]:
        if "stop" in tracker.latest_message.get("text"):
            return [ActiveLoop(None), SlotSet(REQUESTED_SLOT, None)]
        await super().run(dispatcher, tracker, domain)