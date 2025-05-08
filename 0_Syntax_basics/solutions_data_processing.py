"""
Lösungen für die Datenverarbeitungsübungen in Python

Diese Datei enthält Lösungen zum Laden, Verarbeiten und
Visualisieren von CSV-Dateien mit pandas und matplotlib.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt



def aufgabe0():
    """
    Erstellt eine Liste mit allen CSV-Dateinamen in einem Verzeichnis.
    
    Returns:
        list: Liste mit allen CSV-Dateinamen
    """
    verzeichnis = '/home/wowra/repos/pharma-python-basics/simulated_data/data'  # Testverzeichnis
    
    # Prüfen ob Verzeichnis existiert
    if not os.path.exists(verzeichnis):
        print(f"Warnung: Verzeichnis {verzeichnis} existiert nicht!")
        return []
    
    # Alle Dateien im Verzeichnis auflisten
    alle_dateien = os.listdir(verzeichnis)
    
    # Nur CSV-Dateien filtern
    csv_dateien = []
    for datei in alle_dateien:
        if datei.lower().endswith('.csv'):
            csv_dateien.append(datei)

    print(f"{len(csv_dateien)} CSV-Dateien gefunden.")
    return csv_dateien


def aufgabe1(csv_liste, verzeichnis):
    """
    Erstellt den vollständigen Pfad zur ersten CSV-Datei in der Liste.
    
    Args:
        csv_liste (list): Liste mit CSV-Dateinamen
        verzeichnis (str): Pfad zum Verzeichnis mit den CSV-Dateien
    
    Returns:
        str: Vollständiger Pfad zur ersten CSV-Datei
    """
    if not csv_liste:
        print("Keine CSV-Dateien in der Liste!")
        return ""
    
    # Erste Datei aus der Liste nehmen
    erste_datei = csv_liste[0]
    
    # Vollständigen Pfad erstellen
    # Hinweis: In Windows sollte ein 'r' vor dem String stehen oder \\ verwendet werden
    # z.B. r'C:\Daten\' oder 'C:\\Daten\\'
    vollständiger_pfad = os.path.join(verzeichnis, erste_datei)
    
    print(f"Vollständiger Pfad: {vollständiger_pfad}")
    return vollständiger_pfad


def aufgabe2(dateipfad):
    """
    Öffnet die CSV-Datei mit pandas und gibt x- und y-Werte zurück.
    
    Args:
        dateipfad (str): Pfad zur CSV-Datei
    
    Returns:
        tuple: (x, y) als pandas Series oder NumPy arrays
    """
    # Prüfen ob Datei existiert
    if not os.path.exists(dateipfad):
        print(f"Fehler: Datei {dateipfad} existiert nicht!")
        return None, None
    
    try:
        # CSV-Datei mit pandas einlesen
        df = pd.read_csv(dateipfad)
        
        # Prüfen ob die Spalten 'x' und 'y' existieren
        if 'x' not in df.columns or 'y' not in df.columns:
            # Falls nicht, nehmen wir die ersten beiden Spalten
            spalten = df.columns
            if len(spalten) < 2:
                print(f"Warnung: Datei hat weniger als 2 Spalten!")
                return None, None
            
            x = df.iloc[:, 0]  # Erste Spalte
            y = df.iloc[:, 1]  # Zweite Spalte
            print(f"Verwende Spalten {spalten[0]} und {spalten[1]} als x und y.")
        else:
            # Extrahiere die 'x' und 'y' Spalten
            x = df['x']
            y = df['y']
            
        print(f"Daten erfolgreich geladen: {len(x)} Datenpunkte.")
        return x, y
    
    except Exception as e:
        print(f"Fehler beim Laden der Datei: {e}")
        return None, None


def aufgabe3(x, y, titel="Datenpunkte"):
    """
    Erstellt einen einfachen Plot der x- und y-Werte.
    
    Args:
        x: x-Werte als Liste, NumPy array oder pandas Series
        y: y-Werte als Liste, NumPy array oder pandas Series
        titel (str): Titel für den Plot
    """
    if x is None or y is None:
        print("Fehler: Keine gültigen Daten zum Plotten vorhanden!")
        return
    
    # Figure erstellen
    plt.figure(figsize=(10, 6))
    
    # Daten plotten
    plt.plot(x, y, 'b-', linewidth=1.5)
    
    # Beschriftungen hinzufügen
    plt.title(titel)
    plt.xlabel('x-Werte')
    plt.ylabel('y-Werte')
    
    # Gitternetz hinzufügen
    plt.grid(True, alpha=0.3)
    
    # Achsenlimits automatisch anpassen
    plt.tight_layout()
    
    # Plot anzeigen
    plt.show()
    
    print(f"Plot '{titel}' erstellt und angezeigt.")


def aufgabe4(verzeichnis, csv_liste):
    """
    Lädt alle x-Werte aus den CSV-Dateien und speichert sie in einer Liste.
    
    Args:
        verzeichnis (str): Pfad zum Verzeichnis mit den CSV-Dateien
        csv_liste (list): Liste mit CSV-Dateinamen
    
    Returns:
        list: Liste mit allen x-Werten (als Listen oder arrays)
    """
    if not csv_liste:
        print("Keine CSV-Dateien in der Liste!")
        return []
    
    alle_x_werte = []
    
    # Fortschrittsanzeige mit tqdm
    print("Lade alle Datensätze:")
    for datei in csv_liste:
        # Vollständigen Pfad erstellen
        dateipfad = os.path.join(verzeichnis, datei)
        
        # Daten laden
        x, _ = aufgabe2(dateipfad)
        
        # x-Werte speichern, falls vorhanden
        if x is not None:
            alle_x_werte.append(x)
    
    print(f"{len(alle_x_werte)} Datensätze erfolgreich geladen.")
    return alle_x_werte


def aufgabe5(alle_x, alle_y, titel="Alle Datensätze"):
    """
    Erstellt einen Plot mit allen Datensätzen.
    
    Args:
        alle_x (list): Liste mit x-Werten für jeden Datensatz
        alle_y (list): Liste mit y-Werten für jeden Datensatz
        titel (str): Titel für den Plot
    """
    if not alle_x or not alle_y or len(alle_x) != len(alle_y):
        print("Fehler: Keine gültigen Daten zum Plotten vorhanden oder x/y-Listen haben unterschiedliche Längen!")
        return
    
    # Figure erstellen
    plt.figure(figsize=(12, 8))
    
    # Farben für die verschiedenen Datensätze
    farben = ['b', 'r', 'g', 'c', 'm', 'y', 'k', 'orange', 'purple', 'brown']
    
    # Alle Datensätze plotten
    for i, (x, y) in enumerate(zip(alle_x, alle_y)):
        farbe = farben[i % len(farben)]  # Zyklische Farbwahl
        plt.plot(x, y, color=farbe, linewidth=1.5, label=f"Datensatz {i+1}")
    
    # Beschriftungen hinzufügen
    plt.title(titel)
    plt.xlabel('x-Werte')
    plt.ylabel('y-Werte')
    
    # Legende hinzufügen
    plt.legend()
    
    # Gitternetz hinzufügen
    plt.grid(True, alpha=0.3)
    
    # Achsenlimits automatisch anpassen
    plt.tight_layout()
    
    # Plot anzeigen
    plt.show()
    
    print(f"Plot '{titel}' mit {len(alle_x)} Datensätzen erstellt und angezeigt.")


# Hauptfunktion zum Testen aller Aufgaben
def main():
    """Testet alle implementierten Aufgaben nacheinander."""
    print("Aufgabe 0: CSV-Dateien im Verzeichnis auflisten")
    verzeichnis = '/home/wowra/repos/pharma-python-basics/simulated_data/data'  # Passe den Pfad an deine Umgebung an
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
    if x is not None and y is not None:
        print(f"Erste 5 x-Werte: {x[:5].values}")
        print(f"Erste 5 y-Werte: {y[:5].values}")
    
    print("\nAufgabe 3: Plotten des ersten Datensatzes")
    aufgabe3(x, y, f"Datensatz aus {csv_liste[0]}")
    
    print("\nAufgabe 4: Alle x-Werte laden")
    alle_x = aufgabe4(verzeichnis, csv_liste)
    print(f"Anzahl geladener Datensätze: {len(alle_x)}")
    
    print("\nAufgabe 5: Alle Datensätze plotten")
    # Lade alle y-Werte
    alle_y = []
    for datei in csv_liste:
        pfad = os.path.join(verzeichnis, datei)
        _, y_values = aufgabe2(pfad)
        alle_y.append(y_values)
    
    aufgabe5(alle_x, alle_y, "Alle Datensätze im Vergleich")
    print("Alle Aufgaben wurden ausgeführt!")


if __name__ == "__main__":
    main()