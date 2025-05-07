# 1. Basisdatentypen in Python
#   1.0 Int
#     - Ganze Zahlen ohne Nachkommastellen
#     - Beispiel: Zählen, Indizes
#     - Funktionen: int(), abs(), pow(), round()
#     - Hinweise: unterstützt Operatoren +, -, *, //, %, **

# Beispiele für Int
ganzzahl = 42
negativ = -7
ergebnis = ganzzahl + negativ  # 35
potenz = ganzzahl ** 2         # 1764 (42²)
rest = ganzzahl % 5            # 2 (Rest bei Division durch 5)
ganzzahldivision = ganzzahl // 5  # 8 (Ganzzahldivision)

#   1.1 Float
#     - Gleitkommazahlen mit Dezimalstellen
#     - Beispiel: Berechnung von Durchschnittswerten, Konzentrationen
#     - Funktionen: float(), round(), abs()
#     - Hinweise: unterstützt Operatoren +, -, *, /, **

# Beispiele für Float
konzentration = 0.05  # mg/mL
volumen = 2.5         # mL
menge = konzentration * volumen  # 0.125 mg
gerundet = round(menge, 3)       # 0.125 (auf 3 Nachkommastellen)

#   1.2 Boolean
#     - Wahrheitswerte True oder False
#     - Beispiel: Bedingungen in if-Anweisungen
#     - Funktionen: bool()
#     - Hinweise: logische Operatoren and, or, not

# Beispiele für Boolean
ist_valid = True
ist_fertig = False
beide_wahr = ist_valid and ist_fertig  # False
mindestens_eine_wahr = ist_valid or ist_fertig  # True
umkehrung = not ist_valid  # False

#   1.3 String
#     - Zeichenketten (auch einzelne Zeichen)
#     - Beispiel: Text, Bezeichner, Proben-IDs
#     - Funktionen: str(), len(), format()
#     - Methoden: .upper(), .lower(), .split(), .replace(), .strip()

# Beispiele für String
proben_id = "A123-B456"
text = "Messwert liegt bei 0.05 mg/mL"
länge = len(proben_id)  # 9 Zeichen
großbuchstaben = proben_id.upper()  # "A123-B456"
teile = proben_id.split("-")  # ["A123", "B456"]
ersetzt = proben_id.replace("A", "X")  # "X123-B456"

# 1.4 Typumwandlung (Casting)
#     - Funktionen: int(), float(), str(), bool()

zahl_string = "123"
zahl = int(zahl_string)  # 123 als Int
float_wert = float(zahl)  # 123.0 als Float
text_wert = str(float_wert)  # "123.0" als String
boolean_wert = bool(zahl)  # True (0 wäre False)

# 1.5 Datentyp herausfinden mit type()
print(type(zahl))  # <class 'int'>
print(type(konzentration))  # <class 'float'>
print(type(ist_valid))  # <class 'bool'>
print(type(proben_id))  # <class 'str'>
