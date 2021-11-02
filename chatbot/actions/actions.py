# This files contains your custom actions which can be used to run
# custom Python code.


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.events import FormValidation, SlotSet, EventType
from rasa_sdk.types import DomainDict
from rasa_sdk.executor import CollectingDispatcher
from algoliasearch.search_client import SearchClient

client = SearchClient.create('BQCT474121', 'b72f4c8a6b93d0afc8221d06c66e1e66')
index = client.init_index('dev_clothes_v2')

ALLOWED_COLORS_GIRLS = ['morado', 'amarillo', 'negro', 'rosado', 'celeste', 'rojo', 'palo de rosa']
ALLOWED_CLOTHES_GIRLS = ['pantalones', 'blusas', 'ternos', 'todos']
ALLOWED_COLORS_BOYS = ['rojo', 'azul', 'beige', 'blanco']
ALLOWED_CLOTHES_BOYS = ['busos', 'camisetas', 'todos']
ALLOWED_GENDERS = ['niños', 'niño', 'niñas', 'niña']


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

    @staticmethod
    def change_name_button(option: str) -> List:
        """Add new button"""

        new_button = 'Ver Todo' if option == 'todos' else option
        return new_button.capitalize()

    @staticmethod
    def is_int(string: Any) -> bool:
        """Check if a string is an integer."""

        try:
            int(string)
            return True
        except ValueError:
            return False
        

    def validate_gender(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `gender` value."""

        if slot_value.lower() not in ALLOWED_GENDERS:
            dispatcher.utter_message(response="utter_ask_gender")
            return {"gender": None}
        else:
            return {"gender": slot_value}


    def validate_color(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `color` value."""

        gender = tracker.get_slot("gender")

        intent_name = tracker.latest_message["intent"]["name"]
        if intent_name == 'deny':
            return {"color": slot_value}

        if gender == 'niña':
            if slot_value.lower() not in ALLOWED_COLORS_GIRLS:
                dispatcher.utter_message(text = f"Por el momento disponemos de colores como: \n- Morado\n- Amarillo\n- Negro\n- Rosado\n- Celeste\n- Rojo\n- Palo de Rosa")
                return {"color": None}
            else:
                return {"color": slot_value}
            

        if gender == 'niño':
            if slot_value.lower() not in ALLOWED_COLORS_BOYS:
                dispatcher.utter_message(text = f"Por el momento disponemos de colores como: \n- Rojo\n- Azul\n- Beige\n- Blanco")
                return {"color": None}
            else:
                return {"color": slot_value}

    def validate_preferences(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `preferences` value."""

        intent_name = tracker.latest_message["intent"]["name"]
        if intent_name == 'deny':
            return {"preferences": 'no'}
        else:
            return {"preferences": slot_value}

    def validate_category(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `category` value."""
        gender = tracker.get_slot("gender")
        print('category', slot_value)

        if gender == 'niña':
            if slot_value.lower() not in ALLOWED_CLOTHES_GIRLS:
                buttons =[{"title": self.change_name_button(p), "payload": p} for p in ALLOWED_CLOTHES_GIRLS]
                dispatcher.utter_message(text = f"Te cuento que contamos con los siguientes tipos de ropa para niñas:",
                buttons=buttons)
                return {"category": None}
            else:
                dispatcher.utter_message(text=f"Excelente elección 👍🏻")
                return {"category": slot_value}

        if gender == 'niño':
            if slot_value.lower() not in ALLOWED_CLOTHES_BOYS:
                buttons =[{"title": self.change_name_button(p), "payload": p} for p in ALLOWED_CLOTHES_BOYS]
                dispatcher.utter_message(text = f"Te cuento que contamos con los siguientes tipos de ropa para niños:",
                buttons=buttons)
                return {"category": None}
            else:
                dispatcher.utter_message(text=f"Excelente elección 👍🏻")
                return {"category": slot_value}
    
    def validate_number(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `number` value."""

        if self.is_int(slot_value) and int(slot_value) > 0:
            return {"number": slot_value}
        else:
            gender = tracker.get_slot("gender")
            if gender == 'niña':
                dispatcher.utter_message(text = f"Tenemos ropa para niñas de 1 a 8 años:")
            if gender == 'niño':
                dispatcher.utter_message(text = f"Tenemos ropa para niños de 1 a 6 años:")
            return {"number": None}

        

class AskForCategoryAction(Action):

    @staticmethod
    def change_name_button(option: str) -> List:
        """Add new button"""

        new_button = 'Ver Todo' if option == 'todos' else option
        return new_button.capitalize()

    def name(self) -> Text:
        return "action_ask_category"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:

        gender = tracker.get_slot("gender")

        if gender == 'niña':
            buttons =[{"title": self.change_name_button(p) , "payload": p} for p in ALLOWED_CLOTHES_GIRLS]
            dispatcher.utter_message(text = f"Te cuento que contamos con los siguientes tipos de ropa para niñas 👧🏻:", buttons=buttons)
        else:
            buttons =[{"title": self.change_name_button(p), "payload": p} for p in ALLOWED_CLOTHES_BOYS]

            dispatcher.utter_message(text = f"Te cuento que contamos con los siguientes tipos de ropa para niños 👦🏻:", buttons=buttons)

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
            dispatcher.utter_message(json_message=message)

            slots_to_reset = ["gender", "number", "color", "category", "preferences"]
            return [SlotSet(slot, None) for slot in slots_to_reset]
        else:
            # provide out of stock
            text = (
                f"No disponemos de ese producto en específico. Pero puedes seguir buscando..."
            )
            dispatcher.utter_message(text=text)

            slots_to_reset = ["gender", "number", "color", "category", "preferences"]
            return [SlotSet(slot, None) for slot in slots_to_reset]
