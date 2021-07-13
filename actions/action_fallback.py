# ==================================================================
# Action Fallback - implementa mensagens personalizadas para o
# default fallback
# ==================================================================
from .__init__ import *

from random import choice
from rasa_sdk.events import UserUtteranceReverted
import time


class ActionDefaultFallback(Action):
    """Executes the fallback action and goes back to the previous state
    of the dialogue"""

    def name(self) -> Text:
        return "action_default_fallback"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
            ) -> List[Dict[Text, Any]]:

        text = tracker.latest_message['text']
        emoji = False
        is_str = False
        for i in text:
            if i in list_emoji:
                emoji = True
            else:
                is_str = True

        if emoji and is_str is not True:
            dispatcher.utter_message(
                'Ainda não consigo me comunicar por emoji 😔')
            return [UserUtteranceReverted()]

        variacao = choice(
            [
                "Ops...",
                "Poxa...",
                "Poxa vida...",
                "Foi mal...",
                "Desculpa..."
            ]
        )


        events = [e['name'] for e in tracker.events if e['event']
            == 'action' and e['name'] not in ['action_listen']]
        if len(set(events)) <= 1:

            horas = time.strftime('%H', time.localtime())
            minutos = time.strftime('%M', time.localtime())
            segundos = time.strftime('%S', time.localtime())
            
            if horas < '12' and minutos <='59' and segundos <='59':
                dispatcher.utter_message('Bom dia, Bem vindo à secretaria digital FATEC Mogi Mirim')
            elif horas < '18' and minutos <='59' and segundos <='59':
                dispatcher.utter_message('Boa tarde, Bem vindo à secretaria digital FATEC Mogi Mirim')
            elif horas < '24' and minutos <='59' and segundos <='59':
                dispatcher.utter_message('Boa noite, Bem vindo à secretaria digital FATEC Mogi Mirim')
                
            dispatcher.utter_message(
                choice(
                    [
                        f"Em que posso te ajudar? 😊",
                        f"Posso ajudar? 😃",
                        f"Gostaria de uma ajuda? 🙂",
                        f"Como posso atendê-lo(a)? 🤝",
                        f"Como posso te ajudar hoje? 🤝",
                    ]
                )
            )

        elif events[-1] != self.name():
            dispatcher.utter_message(
                choice(
                    [
                        f"{variacao} me desculpe, mas não consegui entender.",
                        "Desculpe, mas não consegui entender o que você disse.",
                        "Não entendi muito bem o que você disse, ainda estou aprendendo.",
                        f"{variacao}, não entendi o que você quis dizer, tente repetir de outra forma.",
                        f"{variacao}, não achei o que você está procurando."
                    ]
                )
            )
            dispatcher.utter_message(
                "Tente me escrever o que precisa com outras palavras...")
        elif events[-2] != self.name():
                dispatcher.utter_message(
                    choice(
                        [
                            f"{variacao} ainda não consegui entender.",
                            "Ainda não consegui entender.",
                            "Ainda não ficou muito claro.",
                            "Ainda não achei o que você está procurando.",
                            f"{variacao} ainda não entendi."
                        ]
                    )
                )
                dispatcher.utter_message(
                    "Tente me escrever o que precisa com outras palavras...")
        else:
                dispatcher.utter_message("Realmente não consegui entender. 😕")
                dispatcher.utter_message("Tente me escrever o que precisa com outras palavras...")

        # Revert user message which led to fallback.
        return [UserUtteranceReverted()]
