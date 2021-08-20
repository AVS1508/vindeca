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

class ValidateForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_form_coronavirus_assessment"
    
    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[EventType]:
        if "stop" in tracker.latest_message.get("text"):
            return [ActiveLoop(None), SlotSet(REQUESTED_SLOT, None)]
        await super().run(dispatcher, tracker, domain)