#!/usr/bin/env python3
"""
Einfaches Skript zum Laden und Plotten eines Chromatogramms
mit Savitzky-Golay-Baseline.
"""
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

# === Einstellungen ===
csv_path = '/home/jannis/repos/pharma-python-basics/simulated_data/data/chromatogram-01.csv'
window_length = 11  # ungerade Zahl > polyorder
polyorder = 3        # Grad des Polynoms
# ======================

df = pd.read_csv(csv_path)
x = df['x']
y = df['y']

baseline = savgol_filter(y, window_length, polyorder)

plt.figure(figsize=(10, 6))
plt.plot(x, y, label='Signal')
plt.plot(x, baseline, '--', label='Baseline (SG)')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Chromatogramm mit Savitzky-Golay-Baseline')
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()
