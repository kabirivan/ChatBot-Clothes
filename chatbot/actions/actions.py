# This files contains your custom actions which can be used to run
# custom Python code.


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.events import FormValidation, SlotSet
from rasa_sdk.types import DomainDict
from rasa_sdk.executor import CollectingDispatcher
from algoliasearch.search_client import SearchClient

client = SearchClient.create('BQCT474121', 'b72f4c8a6b93d0afc8221d06c66e1e66')
index = client.init_index('dev_clothes_v2')

ALLOWED_COLORS_GIRLS = ['morado', 'amarillo', 'negro', 'rosado', 'celeste', 'rojo', 'palo de rosa']
ALLOWED_CLOTHES_GIRLS = ['Pantalones', 'Blusas', 'Ternos']
ALLOWED_COLORS_BOYS = ['rojo', 'azul', 'beige', 'blanco']
ALLOWED_CLOTHES_BOYS = ['Busos']


class ActionHelloWorld(Action):
    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")

        return []


class ValidateClothesForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_clothes_form"

    
    def validate_color(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `color` value."""
        gender = tracker.get_slot("gender")

        if gender == 'niña':
            if slot_value.lower() not in ALLOWED_COLORS_GIRLS:
                print('color', slot_value.lower())
                dispatcher.utter_message(text = f"Por el momento disponemos de colores como: \n- Morado\n- Amarillo\n- Negro\n- Rosado\n- Celeste\n- Rojo\n- Palo de Rosa")
                return {"color": None}
            dispatcher.utter_message(text=f"Ok! El color **{slot_value}** es una gran elección.")

    def validate_category(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `category` value."""
        gender = tracker.get_slot("gender")

        if gender == 'niña':
            if slot_value.lower() not in ALLOWED_CLOTHES_GIRLS:
                dispatcher.utter_message(text = f"Te cuento que contamos con los siguientes tipos de ropa para niñas: \n- Pantalones\n- Blusas\n- Ternos")
                return {"category": None}
            dispatcher.utter_message(text=f"Ok! El color **{slot_value}** es una gran elección.")


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

        if clothes[0] == 'niño':
            clothes[0] = 'M'
        else:
            clothes[0] = 'F'

        print(clothes)
        objects = index.search("", {
            "facetFilters": [
                [
                    "gender:{0[0]}".format(clothes)
                ],
                [
                    "age:{0[1]}".format(clothes)
                ],
                [
                    "category:{0[2]}".format(clothes)
                ],
                [
                    "color:{0[3]}".format(clothes)
                ],
            ]
        })

        print(objects)

        clothes = objects['hits']

        product = []
        for x in clothes:
            print(x['name'])
            product.append({'title': x['name'], 'subtitle': "{0}\nStock: {1} disponibles \nPrecio: {2}".format(x['material'], x['quantity'], x['price']), "image_url": x['image'], "buttons": [
                {
                    "title": "Comprar",
                    "url": "https://www.instagram.com/creacionesjasmina/",
                    "type": "web_url"
                }
            ]})

        message = {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": product
                }
            }
        }


        if clothes:
            # provide in stock message
            text = (
                f"Tenemos algunos productos que te pueden interesar"
            )
            dispatcher.utter_message(json_message=message)

            slots_to_reset = ["gender", "number", "color", "category", "preferences"]
            return [SlotSet(slot, None) for slot in slots_to_reset]
        else:
            # provide out of stock
            text = (
                f"No disponemos de ese producto en específico. Pero puedes seguir buscando"
            )
            dispatcher.utter_message(text=text)

            slots_to_reset = ["gender", "number", "color", "category", "preferences"]
            return [SlotSet(slot, None) for slot in slots_to_reset]
