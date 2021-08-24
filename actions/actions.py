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

class ActionResetSlots(Action):
    def name(self) -> Text:
        return "action_reset_slots"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text,Any]]:
        return [AllSlotsReset()]

class UtterCoronavirusAssessment(Action):
    def name(self) -> Text:
        return "explain_coronavirus_assessment"
    
    def helper_count(self, boolList: List[bool]) -> int:
        counter = 0
        for boolean in boolList:
            counter = counter + 1 if boolean else counter
        return counter
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text,Any]]:
        adverseFactors = [tracker.slots.get("4_past_infection", None) == "true", tracker.slots.get("5_current_symptoms", None) == "true", tracker.slots.get("6_preexisting_conditions", None) == "true", tracker.slots.get("7_travel_interstate", None) == "true"]
        significance = self.helper_count(adverseFactors)
        if tracker.slots.get("3_num_doses", None) == '2':
            if (significance >= 2):
                dispatcher.utter_message("Your infection risk is LOW as you are fully vaccinated with no/few adverse factors. We still recommend that you stay at home to avoid any chance of exposure to the Novel Coronavirus!")
            else:
                dispatcher.utter_message("Your infection risk is MEDIUM as you are fully vaccinated with significant adverse factors. We still strongly recommend that you stay at home to avoid any chance of exposure to the Novel Coronavirus!")
        elif tracker.slots.get("3_num_doses", None) == '1':
            if (significance >= 2):
                dispatcher.utter_message("Your infection risk is MEDIUM as you are partially vaccinated with no/few adverse factors. We recommend that you stay at home to avoid any chance of exposure to the Novel Coronavirus, and receive your 2nd dose at the earliest!")
            else:
                dispatcher.utter_message("Your infection risk is HIGH as you are partially vaccinated with significant adverse factors. We strongly recommend that you stay at home to avoid any chance of exposure to the Novel Coronavirus, and receive your 2nd dose at the earliest!")
        elif tracker.slots.get("3_num_doses", None) == '0':
            if (significance >= 2):
                dispatcher.utter_message("Your infection risk is HIGH as you are not vaccinated but have no/few adverse factors. We strongly advise you to stay at home to avoid any chance of exposure to the Novel Coronavirus, and get started with your vaccinations soon!")
            else:
                dispatcher.utter_message("Your infection risk is VERY HIGH as you are not vaccinated and have significant adverse factors. We strictly advise you to stay at home to avoid any chance of exposure to the Novel Coronavirus, and get started with your vaccinations soon!")
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