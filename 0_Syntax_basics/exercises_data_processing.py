"""
Übungen zur Datenverarbeitung in Python

Diese Datei enthält Übungsaufgaben zum Laden, Verarbeiten und
Visualisieren von CSV-Dateien mit pandas und matplotlib.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt


def aufgabe0():
    """
    Erstellt eine Liste mit allen CSV-Dateinamen in einem Verzeichnis.
    
    Hinweis: Verwende os.listdir() und filter die Ergebnisse auf .csv-Dateien
    
    Returns:
        list: Liste mit allen CSV-Dateinamen
    """
    # TODO: Implementiere diese Funktion
    # Verwende als Testverzeichnis: './daten'
    
    return []


def aufgabe1(csv_liste, verzeichnis):
    """
    Erstellt den vollständigen Pfad zur ersten CSV-Datei in der Liste.
    
    Hinweis: Für Windows-Pfade sollte r'' oder '\\' verwendet werden
    
    Args:
        csv_liste (list): Liste mit CSV-Dateinamen
        verzeichnis (str): Pfad zum Verzeichnis mit den CSV-Dateien
    
    Returns:
        str: Vollständiger Pfad zur ersten CSV-Datei
    """
    # TODO: Implementiere diese Funktion
    
    return ""


def aufgabe2(dateipfad):
    """
    Öffnet die CSV-Datei mit pandas und gibt x- und y-Werte zurück.
    
    Args:
        dateipfad (str): Pfad zur CSV-Datei
    
    Returns:
        tuple: (x, y) als pandas Series oder NumPy arrays
    """
    # TODO: Implementiere diese Funktion
    
    return None, None


def aufgabe3(x, y, titel="Datenpunkte"):
    """
    Erstellt einen einfachen Plot der x- und y-Werte.
    
    Args:
        x: x-Werte als Liste, NumPy array oder pandas Series
        y: y-Werte als Liste, NumPy array oder pandas Series
        titel (str): Titel für den Plot
    """
    # TODO: Implementiere diese Funktion
    # Verwende matplotlib.pyplot zum Erstellen des Plots


def aufgabe4(verzeichnis, csv_liste):
    """
    Lädt alle x-Werte aus den CSV-Dateien und speichert sie in einer Liste.
    
    Args:
        verzeichnis (str): Pfad zum Verzeichnis mit den CSV-Dateien
        csv_liste (list): Liste mit CSV-Dateinamen
    
    Returns:
        list: Liste mit allen x-Werten (als Listen oder arrays)
    """
    # TODO: Implementiere diese Funktion
    # Verwende die Funktion aufgabe2() zum Laden der Daten
    
    return []


def aufgabe5(alle_x, alle_y, titel="Alle Datensätze"):
    """
    Erstellt einen Plot mit allen Datensätzen.
    
    Args:
        alle_x (list): Liste mit x-Werten für jeden Datensatz
        alle_y (list): Liste mit y-Werten für jeden Datensatz
        titel (str): Titel für den Plot
    """
    # TODO: Implementiere diese Funktion
    # Zeichne jeden Datensatz in einer anderen Farbe
    # Füge eine Legende mit Dateinamen hinzu


# Hauptfunktion zum Testen aller Aufgaben
def main():
    """Testet alle implementierten Aufgaben nacheinander."""
    print("Aufgabe 0: CSV-Dateien im Verzeichnis auflisten")
    verzeichnis = './daten'  # Passe den Pfad an deine Umgebung an
    csv_liste = aufgabe0()
    print(f"Gefundene CSV-Dateien: {csv_liste}")
    
    if not csv_liste:
        print("Keine CSV-Dateien gefunden. Beende Programm.")
        return
    
    print("\nAufgabe 1: Vollständigen Pfad erstellen")
    dateipfad = aufgabe1(csv_liste, verzeichnis)
    print(f"Pfad zur ersten Datei: {dateipfad}")
    
    print("\nAufgabe 2: CSV-Datei öffnen und x, y auslesen")
    x, y = aufgabe2(dateipfad)
    print(f"Erste 5 x-Werte: {x[:5]}")
    print(f"Erste 5 y-Werte: {y[:5]}")
    
    print("\nAufgabe 3: Plotten des ersten Datensatzes")
    aufgabe3(x, y, f"Datensatz aus {csv_liste[0]}")
    
    print("\nAufgabe 4: Alle x-Werte laden")
    alle_x = aufgabe4(verzeichnis, csv_liste)
    print(f"Anzahl geladener Datensätze: {len(alle_x)}")
    
    print("\nAufgabe 5: Alle Datensätze plotten")
    # Hier müsstest du alle_y auch laden, was in der Aufgabenstellung fehlt
    # Als Workaround könnten wir aufgabe2() für jeden Datensatz aufrufen
    alle_y = []
    for datei in csv_liste:
        pfad = os.path.join(verzeichnis, datei)
        _, y_values = aufgabe2(pfad)
        alle_y.append(y_values)
    
    aufgabe5(alle_x, alle_y, "Alle Datensätze im Vergleich")
    print("Alle Aufgaben wurden ausgeführt!")


if __name__ == "__main__":
    main()
