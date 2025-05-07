# 2. Collection-Datentypen in Python
#   2.0 Liste (list)
#     - Veränderbare geordnete Sammlung
#     - Beispiel: dynamische Datenlisten, Messwerte
#     - Funktionen: list(), len(), sorted(), sum(), min(), max()
#     - Methoden: .append(), .extend(), .insert(), .remove(), .pop(), .sort()

# Beispiele für Listen
messwerte = [0.5, 0.48, 0.52, 0.49, 0.51]
proben_ids = ["A1", "A2", "A3", "B1", "B2"]

# Listenzugriff
erster_messwert = messwerte[0]  # 0.5 (Indexierung beginnt bei 0)
letzter_messwert = messwerte[-1]  # 0.51 (negativer Index zählt von hinten)
teilmenge = messwerte[1:3]  # [0.48, 0.52] (Slicing: inkl. Start, exkl. Ende)

# Listenoperationen
messwerte.append(0.53)  # Fügt Element am Ende hinzu: [0.5, 0.48, 0.52, 0.49, 0.51, 0.53]
messwerte.insert(1, 0.47)  # Fügt Element an Position 1 ein: [0.5, 0.47, 0.48, 0.52, 0.49, 0.51, 0.53]
messwerte.remove(0.52)  # Entfernt Element: [0.5, 0.47, 0.48, 0.49, 0.51, 0.53]
letzter = messwerte.pop()  # Entfernt und gibt letztes Element zurück: 0.53

# Listenfunktionen
anzahl = len(messwerte)  # 5 Elemente
summe = sum(messwerte)  # 2.45
minimum = min(messwerte)  # 0.47
maximum = max(messwerte)  # 0.51
sortiert = sorted(messwerte)  # [0.47, 0.48, 0.49, 0.5, 0.51] (neue sortierte Liste)
messwerte.sort()  # Sortiert die Liste selbst

#   2.1 Tuple
#     - Unveränderbare geordnete Sammlung
#     - Beispiel: feste Konfigurationen, Koordinaten
#     - Funktionen: tuple(), len(), sum()
#     - Methoden: .count(), .index()

# Beispiele für Tuple
kalibrierungspunkte = (0.0, 0.1, 0.2, 0.5, 1.0)  # unveränderbar!
xyz_koordinate = (12.5, 8.3, 0.7)

# Tupelzugriff (ähnlich wie Listen)
x_wert = xyz_koordinate[0]  # 12.5

# Unpacking: Mehrere Variablen gleichzeitig zuweisen
x, y, z = xyz_koordinate  # x=12.5, y=8.3, z=0.7

# Tuple in Listen umwandeln (und umgekehrt)
punkte_liste = list(kalibrierungspunkte)  # [0.0, 0.1, 0.2, 0.5, 1.0]
punkte_liste.append(2.0)  # [0.0, 0.1, 0.2, 0.5, 1.0, 2.0]
neues_tuple = tuple(punkte_liste)  # (0.0, 0.1, 0.2, 0.5, 1.0, 2.0)

#   2.2 Dictionary (dict)
#     - Schlüssel-Wert-Paare ohne feste Reihenfolge
#     - Beispiel: strukturierte Daten, Zuordnungen
#     - Funktionen: dict(), len()
#     - Methoden: .keys(), .values(), .items(), .update(), .pop()

# Beispiele für Dictionary
probe_daten = {
    "ID": "XYZ-123",
    "Konzentration": 0.05,
    "pH-Wert": 7.4,
    "Temperatur": 25.0,
    "gültig": True
}

# Dictionary-Zugriff
probe_id = probe_daten["ID"]  # "XYZ-123"
konzentration = probe_daten["Konzentration"]  # 0.05

# Dictionary-Operationen
probe_daten["Datum"] = "2025-05-07"  # Neues Schlüssel-Wert-Paar hinzufügen
probe_daten["pH-Wert"] = 7.2  # Wert aktualisieren
temperatur = probe_daten.pop("Temperatur")  # Entfernt und gibt Wert zurück: 25.0

# Dictionary-Methoden
alle_schlüssel = probe_daten.keys()  # dict_keys(['ID', 'Konzentration', 'pH-Wert', 'gültig', 'Datum'])
alle_werte = probe_daten.values()  # dict_values(['XYZ-123', 0.05, 7.2, True, '2025-05-07'])
alle_paare = probe_daten.items()  # dict_items([('ID', 'XYZ-123'), ('Konzentration', 0.05), ...])

# Über Dictionary iterieren
for schlüssel, wert in probe_daten.items():
    print(f"{schlüssel}: {wert}")






# 2.4 Anwendungsbeispiel: Kombinierte Verwendung
analysen = [
    {"probe": "A1", "werte": [0.052, 0.051, 0.053], "status": "valid"},
    {"probe": "A2", "werte": [0.078, 0.079, 0.077], "status": "valid"},
    {"probe": "B1", "werte": [0.041, 0.080, 0.042], "status": "fehler"}
]

# Nur gültige Proben auswählen und Mittelwerte berechnen
gültige_mittelwerte = {}
for analyse in analysen:
    if analyse["status"] == "valid":
        mittelwert = sum(analyse["werte"]) / len(analyse["werte"])
        gültige_mittelwerte[analyse["probe"]] = round(mittelwert, 4)

print(gültige_mittelwerte)  # {'A1': 0.052, 'A2': 0.078}
