# Einfache Gehaltsbestimmung mit Kalibrationsgerade
# Installation: pip install numpy scipy matplotlib

import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# Funktion zur Simulation von Kalibrationsdaten
def erzeuge_kalibrationsdaten(konzentrationen, steigung=0.245, offset=0.008, rauschen=0.002):
    """
    Erzeugt Kalibrationsdaten (z.B. Absorptionswerte) für eine Analysenmethode.
    
    Parameter:
        konzentrationen: NumPy-Array mit Konzentrationen [mg/mL]
        steigung: Empfindlichkeit des Nachweises (default: 0.245 AU·mL/mg)
        offset: Leerwert/Offset (default: 0.008 AU)
        rauschen: Stärke des zufälligen Rauschens (default: 0.002 AU)
    
    Rückgabe:
        NumPy-Array mit Messsignalen (z.B. Absorption)
    """
    # Kalibrationsgerade: Signal = Steigung · Konzentration + Offset
    signale_basis = steigung * konzentrationen + offset
    
    # Zufälliges Rauschen hinzufügen
    if rauschen > 0:
        zufallswerte = np.random.normal(0, rauschen, size=len(konzentrationen))
        signale = signale_basis + zufallswerte
    else:
        signale = signale_basis
    
    return signale

# Funktion zur Berechnung des Gehalts einer Probe
def berechne_gehalt(signal, steigung, offset, verdünnungsfaktor=1.0, einwaage=1.0, 
                   volumen=10.0):
    """
    Berechnet den Gehalt einer Probe basierend auf dem Signal und der Kalibrationsgerade.
    
    Parameter:
        signal: Gemessenes Signal (z.B. Absorption)
        steigung: Steigung der Kalibrationsgerade
        offset: Offset/Leerwert der Kalibrationsgerade
        verdünnungsfaktor: Verdünnungsfaktor der Probenlösung (default: 1.0)
        einwaage: Einwaage der Probe in g (default: 1.0)
        volumen: Volumen der Probenlösung in mL (default: 10.0)
    
    Rückgabe:
        Float: Berechneter Gehalt in mg/g
    """
    # Berechnung der Konzentration [mg/mL] aus dem Signal
    konzentration = (signal - offset) / steigung
    
    # Berechnung des Gehalts unter Berücksichtigung der Probenvorbereitung
    gehalt = konzentration * volumen * verdünnungsfaktor / einwaage
    
    return gehalt

# Hauptprogramm
if __name__ == "__main__":
    # 1. Kalibrationsdaten erstellen
    # Kalibrationsstandards in mg/mL
    konzentrationen = np.array([0.0, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5])
    
    # Signale (z.B. Absorption) für die Kalibrationsstandards simulieren
    signale = erzeuge_kalibrationsdaten(konzentrationen, rauschen=0.002)
    
    # 2. Lineare Regression für die Kalibrationsgerade
    steigung, offset, r_wert, p_wert, std_fehler = stats.linregress(konzentrationen, signale)
    
    # Bestimmtheitsmaß (R²) berechnen
    r_squared = r_wert ** 2
    
    # 3. Kalibrationsgerade berechnen
    kalibrationsgerade = steigung * konzentrationen + offset
    
    # 4. Ergebnisse der Kalibration ausgeben
    print("Kalibrationsergebnisse:")
    print(f"Steigung: {steigung:.4f} AU·mL/mg")
    print(f"Offset (Leerwert): {offset:.4f} AU")
    print(f"Bestimmtheitsmaß (R²): {r_squared:.6f}")
    
    # 5. Testprobe simulieren
    testprobe_konz = 0.075  # mg/mL
    testprobe_signal = erzeuge_kalibrationsdaten(
        np.array([testprobe_konz]), 
        steigung=steigung, 
        offset=offset, 
        rauschen=0.003
    )[0]
    
    # 6. Gehalt berechnen
    verdünnungsfaktor = 10.0  # 1:10 Verdünnung
    einwaage = 0.2           # 200 mg Einwaage
    volumen = 25.0           # 25 mL Volumen
    
    testprobe_gehalt = berechne_gehalt(
        testprobe_signal, 
        steigung, 
        offset, 
        verdünnungsfaktor,
        einwaage,
        volumen
    )
    
    # Testprobenergebnisse ausgeben
    print("\nTestprobenergebnisse:")
    print(f"Signal: {testprobe_signal:.4f} AU")
    print(f"Berechnete Konzentration: {(testprobe_signal - offset) / steigung:.4f} mg/mL")
    print(f"Berechneter Gehalt: {testprobe_gehalt:.2f} mg/g")
    
    # 7. Daten und Kalibrationsgerade plotten
    plt.figure(figsize=(10, 6))
    
    # Kalibrationspunkte plotten
    plt.scatter(konzentrationen, signale, color='blue', label='Kalibrationsstandards')
    
    # Testprobe plotten
    plt.scatter([testprobe_konz], [testprobe_signal], color='green', s=80, 
               marker='*', label='Testprobe')
    
    # Kalibrationsgerade plotten
    plt.plot(konzentrationen, kalibrationsgerade, color='red', 
             label=f'Kalibrationsgerade: y = {steigung:.4f}x + {offset:.4f}')
    
    # Textbox mit Ergebnissen
    ergebnis_text = f"Testprobe:\nSignal: {testprobe_signal:.4f} AU\nKonzentration: {(testprobe_signal - offset) / steigung:.4f} mg/mL\nGehalt: {testprobe_gehalt:.2f} mg/g"
    plt.text(0.6 * max(konzentrationen), 0.2 * max(signale), ergebnis_text,
            bbox=dict(facecolor='white', alpha=0.8))
    
    # Beschriftungen und Formatierung
    plt.title('Gehaltsbestimmung mit Kalibrationsgerade', fontsize=14)
    plt.xlabel('Konzentration [mg/mL]', fontsize=12)
    plt.ylabel('Absorption [AU]', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Plot anzeigen
    plt.tight_layout()
    plt.show()
