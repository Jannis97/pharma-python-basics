# Lösungen zu Python-Grundlagen Übungen

# Übung 0: Variablen und einfache Operationen
# ------------------------------------
# Lösung:
ganze_zahl = 42
kommazahl = 0.123
text = "Messwert"

summe = ganze_zahl + kommazahl
differenz = ganze_zahl - kommazahl
produkt = ganze_zahl * kommazahl
quotient = ganze_zahl / kommazahl

print(f"Summe: {summe}")
print(f"Differenz: {differenz}")
print(f"Produkt: {produkt}")
print(f"Quotient: {quotient}")

verkettet = text + ": " + str(ganze_zahl)
print(f"Verketteter String: {verkettet}")


# Übung 1: Vergleichsoperatoren und Bedingungen
# ------------------------------------
# Lösung:
zahl_a = 15
zahl_b = 7

ist_größer = zahl_a > zahl_b
ist_kleiner = zahl_a < zahl_b
ist_gleich = zahl_a == zahl_b
ist_ungleich = zahl_a != zahl_b

print(f"{zahl_a} > {zahl_b}: {ist_größer}")
print(f"{zahl_a} < {zahl_b}: {ist_kleiner}")
print(f"{zahl_a} == {zahl_b}: {ist_gleich}")
print(f"{zahl_a} != {zahl_b}: {ist_ungleich}")

und_verknüpfung = ist_größer and ist_gleich
oder_verknüpfung = ist_größer or ist_gleich

print(f"UND-Verknüpfung: {und_verknüpfung}")
print(f"ODER-Verknüpfung: {oder_verknüpfung}")


# Übung 2: Listen und Basisoperationen
# ------------------------------------
# Lösung:
messwerte = [0.052, 0.048, 0.053, 0.047, 0.051]

summe = sum(messwerte)
durchschnitt = summe / len(messwerte)
größter_wert = max(messwerte)
kleinster_wert = min(messwerte)
sortierte_liste = sorted(messwerte)

print(f"Messwerte: {messwerte}")
print(f"Summe: {summe}")
print(f"Durchschnitt: {durchschnitt}")
print(f"Größter Wert: {größter_wert}")
print(f"Kleinster Wert: {kleinster_wert}")
print(f"Sortierte Liste: {sortierte_liste}")


# Übung 3: Dictionary erstellen und verwenden
# ------------------------------------
# Lösung:
probe = {
    "ID": "A123",
    "Messwert": 0.052,
    "Einheit": "mg/mL",
    "Zeitpunkt": "2025-05-08",
    "Gültig": True
}

print(f"Probe ID: {probe['ID']}")
print(f"Messwert: {probe['Messwert']} {probe['Einheit']}")

# Wert ändern
probe["Messwert"] = 0.055
print(f"Neuer Messwert: {probe['Messwert']} {probe['Einheit']}")

# Neuen Schlüssel/Wert hinzufügen
probe["Kommentar"] = "Wiederholungsmessung"
print(f"Aktualisierte Probe: {probe}")


# Übung 4: Typumwandlung und formattierte Ausgabe
# ------------------------------------
# Lösung:
zahl_string = "123"
kommazahl = 0.123
bool_wert = True

# Typumwandlungen
zahl_int = int(zahl_string)
zahl_float = float(zahl_string)
kommazahl_string = str(kommazahl)
kommazahl_int = int(kommazahl)
bool_int = int(bool_wert)
bool_string = str(bool_wert)

print(f"zahl_string: {zahl_string}, Typ: {type(zahl_string)}")
print(f"zahl_int: {zahl_int}, Typ: {type(zahl_int)}")
print(f"zahl_float: {zahl_float}, Typ: {type(zahl_float)}")
print(f"kommazahl_string: {kommazahl_string}, Typ: {type(kommazahl_string)}")
print(f"kommazahl_int: {kommazahl_int}, Typ: {type(kommazahl_int)}")
print(f"bool_int: {bool_int}, Typ: {type(bool_int)}")
print(f"bool_string: {bool_string}, Typ: {type(bool_string)}")

# Formatierte Ausgabe
formatierte_ausgabe = f"""
Probe:
- Ursprünglicher Zahl-String: {zahl_string}
- Kommazahl (auf 4 Stellen): {kommazahl:.4f}
- Gültigkeitsstatus: {bool_wert}
"""
print(formatierte_ausgabe)


# Übung 5: if-elif-else Anweisungen
# ------------------------------------
# Lösung:
def analysiere_messwert(messwert):
    if messwert < 0.1:
        return "Zu niedrig"
    elif 0.1 <= messwert < 0.5:
        return "Optimal"
    elif 0.5 <= messwert < 0.8:
        return "Erhöht"
    else:
        return "Zu hoch"

# Testfälle
testwerte = [0.05, 0.2, 0.67, 0.9]
for wert in testwerte:
    einstufung = analysiere_messwert(wert)
    print(f"Messwert {wert}: {einstufung}")


# Übung 6: For-Schleife mit verschiedenen Datenstrukturen
# ------------------------------------
# Lösung:
# Liste von Zahlen - nur gerade ausgeben
zahlen = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print("Gerade Zahlen:")
for zahl in zahlen:
    if zahl % 2 == 0:
        print(zahl, end=" ")
print()

# String - Position von 'e' ausgeben
text = "Spektrometrie ist eine analytische Methode"
print("\nPositionen von 'e':")
for i, buchstabe in enumerate(text):
    if buchstabe.lower() == 'e':
        print(f"Position {i}: '{buchstabe}'")

# Dictionary - formatierte Ausgabe
probe_daten = {
    "ID": "B789",
    "Konzentration": 0.0245,
    "pH": 7.4,
    "Temperatur": 25.3,
    "Gültig": True
}
print("\nProbendaten:")
for schlüssel, wert in probe_daten.items():
    print(f"- {schlüssel}: {wert}")


# Übung 7: Kombination von Kontrollstrukturen
# ------------------------------------
# Lösung:
messwerte = [0.05, 0.12, 0.35, 0.51, 0.64, 0.78, 0.92, 0.49, 0.09, 0.22]

kategorien = {
    "Zu niedrig": 0,
    "Optimal": 0,
    "Erhöht": 0,
    "Zu hoch": 0
}

for wert in messwerte:
    if wert < 0.1:
        kategorien["Zu niedrig"] += 1
    elif 0.1 <= wert < 0.5:
        kategorien["Optimal"] += 1
    elif 0.5 <= wert < 0.8:
        kategorien["Erhöht"] += 1
    else:
        kategorien["Zu hoch"] += 1

print("\nAnalyse der Messwerte:")
for kategorie, anzahl in kategorien.items():
    print(f"{kategorie}: {anzahl} Messwerte")
