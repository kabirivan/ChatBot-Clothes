# This files contains your custom actions which can be used to run
# custom Python code.


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from algoliasearch.search_client import SearchClient

client = SearchClient.create('BQCT474121', 'b72f4c8a6b93d0afc8221d06c66e1e66')
index = client.init_index('dev_clothesChildren')


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")

        return []


class ActionProductSearch(Action):
    def name(self) -> Text:
        return "action_product_search"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        # get slots and save as tuple
        clothes = [tracker.get_slot("gender"), tracker.get_slot(
            "number"), tracker.get_slot("category"), tracker.get_slot("color")]

        objects = index.search("", {
            "facetFilters": [
                [
                    "gender:{0[1]}".format(clothes)
                ],
                [
                    "age:{0[2]}".format(clothes)
                ],
                [
                    "category:{0[3]}".format(clothes)
                ],
                [
                    "color:{0[4]}".format(clothes)
                ],
            ]
        })

        print(objects)

        if objects:
            # provide in stock message
            text = (
                f"Tenemos algunos productos que te pueden interesar"
            )
            dispatcher.utter_message(text = text)

            slots_to_reset = ["gender", "number", "color", "category"]
            return [SlotSet(slot, None) for slot in slots_to_reset]
        else:
            # provide out of stock
            text = (
                f"No disponemos de ese producto en específico. Pero puedes seguir buscando"
            )
            dispatcher.utter_message(text = text)

            slots_to_reset = ["gender", "number", "color", "category"]
            return [SlotSet(slot, None) for slot in slots_to_reset]
