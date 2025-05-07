import pandas as pd
from tqdm import tqdm
import os
import matplotlib.pyplot as plt


def read_all_csvs(params):
    """
    Reads all CSV files from the data directory.
    Assumes no header, with first column as x and second as y.

    Args:
        params (dict): Dictionary containing parameters

    Returns:
        dict: Dictionary with filenames as keys and DataFrames as values
    """
    data_dir = params["data_dir"]

    # List files in the data directory
    files = os.listdir(data_dir)

    # Filter for CSV files only
    csv_files = [f for f in files if f.endswith('.csv')]

    # Sort them
    csv_files.sort()

    if not csv_files:
        raise FileNotFoundError("No CSV files found in the data directory")

    # Dictionary to store all dataframes
    all_dfs = {}

    # Read each CSV file
    for csv_file in tqdm(csv_files, desc="Reading CSV files"):
        print(f"Reading file: {csv_file}")

        # Full path to the file
        file_path = os.path.join(data_dir, csv_file)

        # Read the CSV file without header, and with x, y column names
        df = pd.read_csv(file_path, header=None, names=['x', 'y'])

        # Store the dataframe in the dictionary
        all_dfs[csv_file] = df

        print(f"Successfully read {csv_file} with {len(df)} rows and {len(df.columns)} columns")

    return all_dfs


def plot_all_csvs(all_dfs):
    """
    Plots all CSV data.

    Args:
        all_dfs (dict): Dictionary with filenames as keys and DataFrames as values
    """
    # Create a figure with subplots
    fig, axs = plt.subplots(len(all_dfs), 1, figsize=(10, 4 * len(all_dfs)))

    # If there's only one file, axs will not be an array
    if len(all_dfs) == 1:
        axs = [axs]

    # Plot each dataframe
    for i, (filename, df) in enumerate(all_dfs.items()):
        axs[i].plot(df['x'], df['y'])
        axs[i].set_title(filename)
        axs[i].set_xlabel('x')
        axs[i].set_ylabel('y')

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # Define parameters
    params = {
        "data_dir": "data"
    }

    # Read all CSV files
    all_dfs = read_all_csvs(params)

    # Display first few rows of each dataframe
    for filename, df in all_dfs.items():
        print(f"\nFirst 5 rows of {filename}:")
        print(df.head())

    # Plot all data
    plot_all_csvs(all_dfs)