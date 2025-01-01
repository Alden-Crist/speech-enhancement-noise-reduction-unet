import numpy as np
import os

def combine_batches(source_folder, base_name, batch_start, batch_end, batch_step, output_file):
    """
    Combines .npy files from batches and saves them as one file.

    Parameters:
        source_folder (str): Folder containing the batch .npy files.
        base_name (str): Base name of the .npy files (e.g., "noisy_voice_amp_db_batch_").
        batch_start (int): Starting batch index.
        batch_end (int): Ending batch index (inclusive).
        batch_step (int): Step size for batches.
        output_file (str): Path to save the combined file.
    """
    combined_data = []

    # Iterate over the specified batch range
    for i in range(batch_start, batch_end + 1, batch_step):
        file_name = f"{base_name}{i}.npy"
        file_path = os.path.join(source_folder, file_name)
        
        if os.path.exists(file_path):
            print(f"Loading file: {file_path}")
            data = np.load(file_path)
            combined_data.append(data)
        else:
            print(f"File not found: {file_path}. Skipping.")

    # Concatenate all loaded data
    combined_data = np.concatenate(combined_data, axis=0)
    print(f"Combined data shape: {combined_data.shape}")

    # Save the combined data
    np.save(output_file, combined_data)
    print(f"Saved combined file to: {output_file}")

# Define parameters
source_folder = '/Users/alden/OneDrive/Desktop/Data/Train/spectrogram'
output_folder ='/Users/alden/OneDrive/Desktop/Data/Train/spectrogram_data'
# Combine noisy voice files
combine_batches(
    source_folder=source_folder,
    base_name="noisy_voice_amp_db_batch_",
    batch_start=20000,
    batch_end=39000,
    batch_step=1000,
    output_file=os.path.join(output_folder, "noisy_voice_amp_db2.npy")
)

# Combine clean voice files
combine_batches(
    source_folder=source_folder,
    base_name="voice_amp_db_batch_",
    batch_start=20000,
    batch_end=39000,
    batch_step=1000,
    output_file=os.path.join(output_folder, "voice_amp_db2.npy")
)
