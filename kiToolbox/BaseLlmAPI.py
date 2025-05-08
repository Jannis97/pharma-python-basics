import os
import json
import requests
from tqdm import tqdm
from typing import Dict, Any, Optional


def get_token(token_filepath: str) -> str:
    """
    Lädt den Token aus der angegebenen Datei.
    Raises FileNotFoundError oder ValueError, falls Probleme auftreten.
    """
    if not os.path.isfile(token_filepath):
        raise FileNotFoundError(f"Token file '{token_filepath}' not found.")
    with open(token_filepath, 'r', encoding='utf-8') as f:
        token = f.read().strip()
    if not token:
        raise ValueError(f"Token file '{token_filepath}' is empty.")
    return token


class BaseLlmAPI:
    """
    Basisklasse für alle LLM-API-Wrapper.
    Definiert die grundlegende Struktur und gemeinsame Funktionalität.
    """

    def __init__(self, params: Dict[str, Any]):
        """
        Initialisiert die Basis-API mit den übergebenen Parametern.

        Args:
            params (dict): Ein Dictionary mit den folgenden Parametern:
                - token_filepath (str): Pfad zur Datei mit dem API-Token
                - model (str, optional): Zu verwendendes Modell
                - base_url (str, optional): Basis-URL der API
        """
        self.token = get_token(params["token_filepath"])
        self.model = params.get("model", self._get_default_model())
        self.base_url = params.get("base_url", self._get_default_url())
        self.headers = self._get_headers()

    def _get_default_model(self) -> str:
        """
        Gibt das Standardmodell für diese API zurück.
        Muss von den Unterklassen überschrieben werden.
        """
        raise NotImplementedError("Subclasses must implement _get_default_model")

    def _get_default_url(self) -> str:
        """
        Gibt die Standard-URL für diese API zurück.
        Muss von den Unterklassen überschrieben werden.
        """
        raise NotImplementedError("Subclasses must implement _get_default_url")

    def _get_headers(self) -> Dict[str, str]:
        """
        Erzeugt die HTTP-Header für API-Anfragen.
        Muss von den Unterklassen überschrieben werden.
        """
        raise NotImplementedError("Subclasses must implement _get_headers")

    def _create_request_payload(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Erstellt die Payload für die API-Anfrage.
        Muss von den Unterklassen überschrieben werden.
        """
        raise NotImplementedError("Subclasses must implement _create_request_payload")

    def _extract_response_text(self, response_json: Dict[str, Any]) -> str:
        """
        Extrahiert den Textinhalt aus der API-Antwort.
        Muss von den Unterklassen überschrieben werden.
        """
        raise NotImplementedError("Subclasses must implement _extract_response_text")

    def answer_question(self, params: Dict[str, Any]) -> str:
        """
        Stellt eine Frage an die API und gibt die Antwort zurück.

        Args:
            params (dict): Ein Dictionary mit den folgenden Parametern:
                - prompt (str): Die zu stellende Frage
                - model (str, optional): Zu verwendendes Modell
                - max_tokens (int, optional): Maximale Anzahl der Tokens in der Antwort
                - temperature (float, optional): Temperatur für die Antwortgenerierung

        Returns:
            str: Die Antwort des Modells
        """
        # Erstelle Payload für die Anfrage
        payload = self._create_request_payload(params)

        try:
            # Sende Anfrage an die API
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=payload,
                timeout=120  # 2 Minuten Timeout
            )

            # Überprüfe auf Fehler
            response.raise_for_status()
            json_response = response.json()

            # Extrahiere die Antwort
            return self._extract_response_text(json_response)

        except Exception as e:
            print(f"Fehler bei der API-Anfrage: {e}")
            return f"Fehler: {e}"

    def generate_qa(self, params: Dict[str, Any]) -> Dict[str, str]:
        """
        Generiert ein Frage-Antwort-Paar mit dem gegebenen Prompt.

        Args:
            params (dict): Ein Dictionary mit folgenden Schlüsseln:
                - prompt (str): Der Eingabetext für die Frage
                - model (str, optional): Zu verwendende Modell
                - max_tokens (int, optional): Maximale Anzahl der Tokens in der Antwort
                - temperature (float, optional): Temperatur für die Antwortgenerierung

        Returns:
            dict: Dictionary mit Frage und Antwort
        """
        api_name = self.__class__.__name__
        print(f"Generating QA pair with {api_name} for prompt: {params['prompt'][:50]}...")

        response_text = self.answer_question(params)

        return {
            "question": params["prompt"],
            "answer": response_text
        }

    def dict_to_dict(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Konvertiert ein Eingabe-Dictionary in ein anderes Format basierend auf einer KI-Antwort.

        Args:
            params (dict): Ein Dictionary mit folgenden Schlüsseln:
                - input_dict (dict): Das zu konvertierende Eingabe-Dictionary
                - conversion_prompt (str): Anleitung für die Konvertierung
                - model (str, optional): Zu verwendende Modell

        Returns:
            dict: Das konvertierte Dictionary
        """
        api_name = self.__class__.__name__
        print(f"Converting dictionary with {api_name}...")

        input_dict_str = json.dumps(params["input_dict"], ensure_ascii=False, indent=2)
        prompt = f"{params['conversion_prompt']}\n\nEingabe-Dictionary:\n{input_dict_str}\n\nGib nur das resultierende JSON zurück, ohne zusätzlichen Text."

        chat_params = {
            "prompt": prompt,
            "model": params.get("model", self.model),
            "temperature": params.get("temperature", 0.2)  # Niedrigere Temperatur für präzisere Antworten
        }

        response = self.answer_question(chat_params)

        # Versuche, aus der Antwort ein Dictionary zu extrahieren
        try:
            # Suche nach JSON-Blöcken in der Antwort
            json_start = response.find('{')
            json_end = response.rfind('}') + 1

            if json_start >= 0 and json_end > json_start:
                json_str = response[json_start:json_end]
                return json.loads(json_str)
            else:
                print(f"Kein gültiges JSON-Dictionary in der {api_name}-Antwort gefunden.")
                return {"error": "Konvertierung fehlgeschlagen", "raw_response": response}

        except json.JSONDecodeError:
            print(f"Konnte das Antwort-Dictionary von {api_name} nicht analysieren.")
            return {"error": "JSON-Parsing fehlgeschlagen", "raw_response": response}