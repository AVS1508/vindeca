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
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text,Any]]:
        adverseFactors = ["4_past_infection", "5_current_symptoms", "6_preexisting_conditions", "7_travel_interstate"]
        significance = 0
        for factor in adverseFactors:
            if tracker.slots.get(factor, None) == "true":
                significance += 1
        if tracker.slots.get("3_num_doses", None) == '2':
            if (significance < 2):
                dispatcher.utter_message("Your infection risk is LOW as you are fully vaccinated with no/few adverse factors. We still recommend that you stay at home to avoid any chance of exposure to the Novel Coronavirus!")
            else:
                dispatcher.utter_message("Your infection risk is MEDIUM as you are fully vaccinated with significant adverse factors. We still strongly recommend that you stay at home to avoid any chance of exposure to the Novel Coronavirus!")
        elif tracker.slots.get("3_num_doses", None) == '1':
            if (significance < 2):
                dispatcher.utter_message("Your infection risk is MEDIUM as you are partially vaccinated with no/few adverse factors. We recommend that you stay at home to avoid any chance of exposure to the Novel Coronavirus, and receive your 2nd dose at the earliest!")
            else:
                dispatcher.utter_message("Your infection risk is HIGH as you are partially vaccinated with significant adverse factors. We strongly recommend that you stay at home to avoid any chance of exposure to the Novel Coronavirus, and receive your 2nd dose at the earliest!")
        elif tracker.slots.get("3_num_doses", None) == '0':
            if (significance < 2):
                dispatcher.utter_message("Your infection risk is HIGH as you are not vaccinated but have no/few adverse factors. We strongly advise you to stay at home to avoid any chance of exposure to the Novel Coronavirus, and get started with your vaccinations soon!")
            else:
                dispatcher.utter_message("Your infection risk is VERY HIGH as you are not vaccinated and have significant adverse factors. We strictly advise you to stay at home to avoid any chance of exposure to the Novel Coronavirus, and get started with your vaccinations soon!")
        else:
            dispatcher.utter_message("I am still learning how to process this data to estimate your risk levels! Till then, kindly maintain social distancing in public and wear masks extensively in order to protect everyone.")
        return []

class ValidateForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_form_coronavirus_assessment"

    @staticmethod
    def vaccine_db() -> List[Text]:
        return ["covaxin", "covishield", "sputnik", "other", "none"]

    @staticmethod
    def num_doses_db() -> List[Text]:
        return ['0','1','2']
    
    def validate_1_is_vaccinated(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> Dict[Text, Any]:
        return {"1_is_vaccinated": slot_value} if slot_value.lower() in ["yes", "no"] else {"1_is_vaccinated": None}
    
    def validate_2_vaccine_brand(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> Dict[Text, Any]:
        return {"2_vaccine_brand": slot_value} if slot_value.lower() in self.vaccine_db() else {"2_vaccine_brand": None}

    def validate_3_num_doses(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> Dict[Text, Any]:
        return {"3_num_doses": slot_value} if slot_value.lower() in self.num_doses_db() else {"3_num_doses": None}

    def validate_4_past_infection(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> Dict[Text, Any]:
        return {"4_past_infection": slot_value} if slot_value.lower() in ["yes", "no"] else {"4_past_infection": None}

    def validate_5_current_symptoms(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> Dict[Text, Any]:
        return {"5_current_symptoms": slot_value} if slot_value.lower() in ["yes", "no"] else {"5_current_symptoms": None}

    def validate_6_preexisting_conditions(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> Dict[Text, Any]:
        return {"6_preexisting_conditions": slot_value} if slot_value.lower() in ["yes", "no"] else {"6_preexisting_conditions": None}

    def validate_7_travel_interstate(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> Dict[Text, Any]:
        return {"7_travel_interstate": slot_value} if slot_value.lower() in ["yes", "no"] else {"7_travel_interstate": None}

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[EventType]:
        if "stop" in tracker.latest_message.get("text"):
            return [ActiveLoop(None), SlotSet(REQUESTED_SLOT, None)]
        await super().run(dispatcher, tracker, domain)