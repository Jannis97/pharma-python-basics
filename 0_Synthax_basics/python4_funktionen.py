# 4. Funktionen in Python
#   4.0 Funktionsdefinition und -aufruf
#     - Definition mit def Funktionsname(parameter):
#     - Rückgabe mit return
#     - Aufruf mit Funktionsname(argumente)

# Einfache Funktion ohne Parameter
def begrüßung():
    """Gibt eine Begrüßung aus."""
    return "Willkommen zum Analyseprogramm!"

nachricht = begrüßung()
print(nachricht)

# Funktion mit einem Parameter
def berechne_konzentration(messwert):
    """Berechnet die Konzentration basierend auf dem Messwert."""
    faktor = 0.0245  # Umrechnungsfaktor
    return messwert * faktor

absorption = 0.528
konzentration = berechne_konzentration(absorption)
print(f"Bei Absorption {absorption} beträgt die Konzentration {konzentration:.4f} mg/mL")

# Funktion mit mehreren Parametern
def berechne_verdünnung(konzentration, zielverdünnung):
    """Berechnet die notwendigen Volumina für eine Verdünnung."""
    if zielverdünnung <= 0 or zielverdünnung >= 1:
        return "Ungültiger Verdünnungsfaktor"
    
    zielkonzentration = konzentration * zielverdünnung
    return zielkonzentration

ausgangskonzentration = 0.1  # mg/mL
verdünnung = berechne_verdünnung(ausgangskonzentration, 0.5)
print(f"Verdünnte Konzentration: {verdünnung} mg/mL")

#   4.1 Funktionen mit Standardwerten
#     - Parameter können Standardwerte haben
#     - Syntax: def funktion(param=standardwert):

def berechne_statistik(werte, dezimalstellen=2):
    """Berechnet statistische Kennzahlen für eine Liste von Werten."""
    anzahl = len(werte)
    if anzahl == 0:
        return {"mittelwert": None, "minimum": None, "maximum": None}
    
    mittelwert = sum(werte) / anzahl
    minimum = min(werte)
    maximum = max(werte)
    
    return {
        "mittelwert": round(mittelwert, dezimalstellen),
        "minimum": round(minimum, dezimalstellen),
        "maximum": round(maximum, dezimalstellen)
    }

messwerte = [0.052, 0.048, 0.051, 0.049, 0.053]
statistik = berechne_statistik(messwerte)  # Standardwert für dezimalstellen
print(f"Statistik: {statistik}")

# Mit explizitem Parameter
präzise_statistik = berechne_statistik(messwerte, dezimalstellen=4)
print(f"Präzise Statistik: {präzise_statistik}")

