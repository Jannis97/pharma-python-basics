import os
import json
from kiToolbox.KIToolboxAPI import KIToolboxAPI


def main():
    """
    Einfaches Beispielprogramm für die KIToolboxAPI.
    """
    # Aktuelles Verzeichnis ermitteln
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Parameter für die API
    params = {
        "token_filepath": os.path.join(current_dir, "kiToolbox.txt"),
        "model": "gpt-4o"
    }

    print("=== KI-Toolbox API Beispielprogramm ===")

    try:
        # Initialisiere die API
        api = KIToolboxAPI(params)
        print(f"API initialisiert mit Modell: {params['model']}")

        # 1. Beispiel: Einfache Textanfrage
        print("\n=== Text-Beispiel ===")
        text_params = {
            "prompt": "Erkläre SMILES für Anfänger in der Cheminformatik.",
            "model": "gpt-4o"
        }

        print(f"Frage: {text_params['prompt']}")
        print("Generiere Antwort...")

        text_result = api.generate_qa(text_params)
        print(f"Antwort: {text_result['answer']}")

        # 2. Beispiel: Dictionary-Verarbeitung
        print("\n=== Dictionary-Beispiel ===")

        # Einfaches Molekül-Dictionary
        molekül_dict = {
            "name": "Aspirin",
            "smiles": "CC(=O)OC1=CC=CC=C1C(=O)O",
            "molgewicht": 180.16,
            "wirkung": "Schmerzmittel"
        }

        # Anfrage zur Umwandlung des Dictionaries
        dict_params = {
            "input_dict": molekül_dict,
            "conversion_prompt": "Wandle dieses Molekül-Dictionary in ein neues Format um, das mehr Informationen enthält. Füge Felder für 'struktur_typ', 'anwendungsgebiete' und 'chemische_eigenschaften' hinzu.",
            "model": "gpt-4o"
        }

        print("Eingabe-Dictionary:")
        print(json.dumps(molekül_dict, indent=2, ensure_ascii=False))
        print("\nKonvertiere Dictionary...")

        dict_result = api.dict_to_dict(dict_params)
        print("\nErgebnis-Dictionary:")
        print(json.dumps(dict_result, indent=2, ensure_ascii=False))

        print("\n=== Beispiele erfolgreich abgeschlossen! ===")

    except Exception as e:
        print(f"\nFehler bei der Ausführung: {e}")


if __name__ == "__main__":
    main()