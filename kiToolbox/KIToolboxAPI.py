import json
import requests
from tqdm import tqdm
from typing import Dict, Any, List

from kiToolbox.BaseLlmAPI import BaseLlmAPI


class KIToolboxAPI(BaseLlmAPI):
    """
    Wrapper für die KI-Toolbox-API der TU Braunschweig.
    Sendet Prompt und empfängt Streaming- bzw. vollständige Antworten.

    Verfügbare Modelle:
    - gpt-4o (Standard): Das neueste GPT-4 Modell mit optimierter Leistung
    - gpt-4: Das Standardmodell von GPT-4
    - claude-3-opus: Das leistungsstärkste Claude-3 Modell
    """

    def _get_default_model(self) -> str:
        """
        Gibt das Standardmodell für die KI-Toolbox zurück.
        """
        return "gpt-4o"

    def _get_default_url(self) -> str:
        """
        Gibt die Standard-URL für die KI-Toolbox zurück.
        """
        return "https://ki-toolbox.tu-braunschweig.de/api/v1/chat"

    def _get_headers(self) -> Dict[str, str]:
        """
        Erzeugt die HTTP-Header für KI-Toolbox-API-Anfragen.
        """
        return {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}"
        }

    def _create_request_payload(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Erstellt die Payload für die KI-Toolbox-API-Anfrage.
        """
        payload = {
            "prompt": params["prompt"],
            "model": params.get("model", self.model)
        }

        if "thread" in params:
            payload["thread"] = params["thread"]

        return payload

    def _extract_response_text(self, response_json: Dict[str, Any]) -> str:
        """
        Extrahiert den Textinhalt aus der KI-Toolbox-API-Antwort.
        """
        # Bei der KIToolbox-API müssen wir eine Spezialbehandlung vornehmen,
        # da die Antwort in einem anderen Format ist (zeilenweises JSON)
        return self.get_answer_text(self.parse_response(response_json))

    def send_chat(self, params: Dict[str, Any]) -> requests.Response:
        """
        Sendet eine Chat-Anfrage an die KI-Toolbox-API.

        Args:
            params (dict): Parameter für die Anfrage

        Returns:
            requests.Response: Die HTTP-Antwort
        """
        url = f"{self.base_url}/send"
        payload = self._create_request_payload(params)
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response

    def parse_response(self, response: requests.Response) -> List[Dict[str, Any]]:
        """
        Parst die zeilenweise JSON-Antwort der KI-Toolbox-API.

        Args:
            response: Die HTTP-Antwort

        Returns:
            list: Liste der geparsten JSON-Objekte
        """
        parsed = []

        # Bei einem Dictionary (bereits geparst) direkt zurückgeben
        if isinstance(response, dict):
            return [response]

        # Bei einer Response den Text zeilenweise parsen
        for line in response.text.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                parsed.append(json.loads(line))
            except json.JSONDecodeError:
                continue
        return parsed

    def get_answer_text(self, parsed_objects: List[Dict[str, Any]]) -> str:
        """
        Extrahiert den Antworttext aus den geparsten JSON-Objekten.

        Args:
            parsed_objects: Liste der geparsten JSON-Objekte

        Returns:
            str: Der extrahierte Antworttext
        """
        for obj in parsed_objects:
            if obj["type"] == "done" and "response" in obj:
                return obj["response"].strip()
        chunks = [obj["content"] for obj in parsed_objects if obj["type"] == "chunk"]
        return "".join(chunks).strip()

    def answer_question(self, params: Dict[str, Any]) -> str:
        """
        Überschreibt die answer_question-Methode, um die spezielle
        Verarbeitung der KI-Toolbox-API zu verwenden.
        """
        resp = self.send_chat(params=params)
        parsed = self.parse_response(resp)
        return self.get_answer_text(parsed)


def main():
    """
    Testet die KIToolboxAPI-Klasse.
    """
    import os

    # Aktuelles Verzeichnis ermitteln
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Konfiguration
    params = {
        "token_filepath": os.path.join(current_dir, "..", "apiKeys", "kiToolbox.txt"),
        "model": "gpt-4o"
    }

    # Initialisiere API
    try:
        api = KIToolboxAPI(params)

        # Testfrage
        test_params = {
            "prompt": "Was sind die Vorteile von SMILES in der Cheminformatik?",
            "model": "gpt-4o"
        }

        result = api.generate_qa(test_params)

        print("\n=== KI-Toolbox API Test ===")
        print(f"Frage: {result['question']}")
        print(f"Antwort: {result['answer'][:200]}...")  # Zeige nur die ersten 200 Zeichen

        print("\nTest erfolgreich!")

    except Exception as e:
        print(f"Fehler beim Testen der KI-Toolbox API: {e}")


if __name__ == "__main__":
    main()