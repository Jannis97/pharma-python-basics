# Simple Regression and Plotting Example
# Installation: pip install numpy scipy matplotlib

import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# Funktion, die y-Daten für einen x-Vektor erzeugt
def erzeuge_y_daten(x_vektor, steigung=2.5, y_achsenabschnitt=1.0, rauschen=0.5):
    """
    Erzeugt y-Daten basierend auf einer linearen Funktion mit Rauschen.
    
    Parameter:
        x_vektor: NumPy-Array mit x-Werten
        steigung: Steigung der linearen Funktion (default: 2.5)
        y_achsenabschnitt: y-Achsenabschnitt (default: 1.0)
        rauschen: Stärke des zufälligen Rauschens (default: 0.5)
    
    Rückgabe:
        NumPy-Array mit y-Werten
    """
    # Lineare Funktion: y = m*x + b
    y_basis = steigung * x_vektor + y_achsenabschnitt
    
    # Zufälliges Rauschen hinzufügen
    if rauschen > 0:
        zufallswerte = np.random.normal(0, rauschen, size=len(x_vektor))
        y_vektor = y_basis + zufallswerte
    else:
        y_vektor = y_basis
    
    return y_vektor

# Hauptprogramm
if __name__ == "__main__":
    # 1. Erzeuge x-Vektor mit 20 Punkten zwischen 0 und 10
    x = np.linspace(0, 10, 20)
    
    # 2. Erzeuge y-Daten mit unserer Funktion
    y = erzeuge_y_daten(x, steigung=2.0, y_achsenabschnitt=5.0, rauschen=2.0)
    
    # 3. Regression mit scipy.stats.linregress
    steigung, y_achsenabschnitt, r_wert, p_wert, std_fehler = stats.linregress(x, y)
    
    # Bestimmtheitsmaß (R²) berechnen
    r_squared = r_wert ** 2
    
    # 4. Regressionslinie berechnen
    regressionslinie = steigung * x + y_achsenabschnitt
    
    # 5. Ergebnisse ausgeben
    print("Regressionsergebnisse:")
    print(f"Steigung: {steigung:.4f}")
    print(f"y-Achsenabschnitt: {y_achsenabschnitt:.4f}")
    print(f"Bestimmtheitsmaß (R²): {r_squared:.4f}")
    print(f"p-Wert: {p_wert:.6f}")
    print(f"Standardfehler: {std_fehler:.4f}")
    
    # 6. Daten und Regressionslinie plotten
    plt.figure(figsize=(10, 6))
    
    # Datenpunkte plotten
    plt.scatter(x, y, color='blue', label='Messdaten')
    
    # Regressionslinie plotten
    plt.plot(x, regressionslinie, color='red', 
             label=f'Regression: y = {steigung:.2f}x + {y_achsenabschnitt:.2f}')
    
    # Beschriftungen und Formatierung
    plt.title('Lineare Regression', fontsize=14)
    plt.xlabel('x-Werte', fontsize=12)
    plt.ylabel('y-Werte', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Plot anzeigen
    plt.tight_layout()
    plt.show()
