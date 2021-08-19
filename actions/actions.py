# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from typing import Any, Text, Dict, List, Union

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
# from rasa_sdk.forms import FormAction
from rasa_sdk.events import AllSlotsReset

# class FormCoronavirusAssessment(FormAction):
#     def __init__(self):
#         print('Created')

#     def name(self) -> Text:
#         return "form_coronavirus_assessment"

#     @staticmethod
#     def required_slots(tracker: Tracker) -> List[Text]:
#         return ["is_vaccinated", "vaccine_brand", "num_doses", "past_infection", "current_symptoms", "preexisting_conditions", "travel_interstate"]
    
#     def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
#         return {
#             "is_vaccinated": self.from_text(),
#             "vaccine_brand": self.from_text(),
#             "num_doses": self.from_text(),
#             "past_infection": self.from_text(),
#             "current_symptoms": self.from_text(),
#             "preexisting_conditions": self.from_text(),
#             "travel_interstate": self.from_text(),
#         }
    
#     def submit (self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
#         return []

class ActionResetSlots(Action):
    def name(self) -> Text:
        return "action_reset_slots"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text,Any]]:
        return [AllSlotsReset()]
