#!/usr/bin/env python3
"""
Script to load and plot a chromatogram CSV file and estimate the baseline using Savitzky-Golay filter.
"""
import os
import sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter


def main(csv_path=None, window_length=21, polyorder=3):
    # Default path to the first chromatogram file
    if csv_path is None:
        csv_path = '/home/jannis/repos/pharma-python-basics/simulated_data/data/chromatogram-01.csv'

    # Check if file exists
    if not os.path.exists(csv_path):
        print(f"Error: File not found at {csv_path}")
        sys.exit(1)

    # Load data
    df = pd.read_csv(csv_path)
    if 'x' not in df.columns or 'y' not in df.columns:
        print("Error: CSV must contain 'x' and 'y' columns.")
        sys.exit(1)

    x = df['x'].values
    y = df['y'].values

    # Ensure window_length is odd and less than data length
    if window_length >= len(y):
        window_length = len(y) - 1 if len(y) % 2 == 0 else len(y)
    if window_length % 2 == 0:
        window_length -= 1
    if window_length < polyorder + 2:
        window_length = polyorder + 2
        if window_length % 2 == 0:
            window_length += 1

    # Compute baseline with Savitzky-Golay filter
    baseline = savgol_filter(y, window_length=window_length, polyorder=polyorder)

    # Plot
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, label=os.path.basename(csv_path))
    plt.plot(x, baseline, '--', label=f'Baseline (SG, wl={window_length}, poly={polyorder})')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title(f"Chromatogram with Savitzky-Golay Baseline: {os.path.basename(csv_path)}")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    # Allow passing custom CSV path and SG parameters
    import argparse
    parser = argparse.ArgumentParser(description='Plot chromatogram with Savitzky-Golay baseline.')
    parser.add_argument('csv_path', nargs='?', help='Path to CSV file', default=None)
    parser.add_argument('--window', type=int, help='SG window length (odd)', default=21)
    parser.add_argument('--poly', type=int, help='SG polynomial order', default=3)
    args = parser.parse_args()
    main(args.csv_path, args.window, args.poly)
