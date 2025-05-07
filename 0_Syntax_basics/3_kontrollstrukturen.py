# 3. Kontrollstrukturen in Python
#   3.0 Bedingte Anweisungen (if, elif, else)
#     - Ausführen von Code basierend auf Bedingungen
#     - Syntax: if Bedingung:, elif Bedingung:, else:
#     - Verschachtelbare Struktur

# Einfaches Beispiel
messwert = 0.052  # mg/mL
grenzwert = 0.05  # mg/mL

if messwert > grenzwert:
    print(f"Messwert {messwert} überschreitet Grenzwert von {grenzwert}")
    status = "zu hoch"
elif messwert < grenzwert * 0.9:  # 10% unter Grenzwert
    print(f"Messwert {messwert} deutlich unter Grenzwert von {grenzwert}")
    status = "niedrig"
else:
    print(f"Messwert {messwert} nahe am Grenzwert von {grenzwert}")
    status = "grenzwertig"

# Komplexere Bedingungen mit logischen Operatoren
ist_valid = True
ist_wiederholungsmessung = False

if ist_valid and messwert <= grenzwert:
    print("Gültige Messung im akzeptablen Bereich")
elif ist_valid and messwert > grenzwert:
    print("Gültige Messung, aber über dem Grenzwert")
elif not ist_valid and ist_wiederholungsmessung:
    print("Ungültige Wiederholungsmessung, bitte neu durchführen")
else:
    print("Ungültige Messung, bitte wiederholen")

# Einzeilige if-Anweisung (Ternary Operator)
resultat = "bestanden" if messwert <= grenzwert else "nicht bestanden"

#   3.1 Schleifen - for
#     - Iterieren über Sequenzen (Listen, Strings, etc.)
#     - Syntax: for element in sequenz:
#     - Kombinierbar mit range(), enumerate(), zip()

# Einfache for-Schleife über Liste
proben = ["A1", "A2", "A3", "B1", "B2"]
for probe in proben:
    print(f"Analysiere Probe {probe}")

# for-Schleife mit range()
for i in range(5):  # 0, 1, 2, 3, 4
    print(f"Schritt {i+1} von 5")

# for-Schleife mit enumerate() für Index und Wert
for index, probe in enumerate(proben):
    print(f"Probe {index+1}: {probe}")

# for-Schleife mit zip() für parallele Listen
messwerte = [0.052, 0.048, 0.051, 0.047, 0.053]
for probe, messwert in zip(proben, messwerte):
    print(f"Probe {probe}: {messwert} mg/mL")

# for-Schleife mit dictionary
probe_daten = {
    "A1": 0.052,
    "A2": 0.048,
    "A3": 0.051
}
for probe_id, konzentration in probe_daten.items():
    print(f"Probe {probe_id} hat Konzentration {konzentration} mg/mL")

