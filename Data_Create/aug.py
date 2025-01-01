import numpy as np
import soundfile as sf
import os
from scipy.signal import resample

def generate_variations(input_dir, output_dir, num_variations, sample_rate):
    """
    Generate extremely subtle variations (0.5% difference) of all noise samples in a directory
    by adjusting only the volume, ensuring the duration stays the same as the original.

    Args:
        input_dir (str): Path to the directory containing input noise files.
        output_dir (str): Path to the directory to save generated noise variations.
        num_variations (int): Number of noise variations to create for each file.
        sample_rate (int): Sampling rate in Hz.

    Returns:
        None
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # List all input noise files
    input_files = [f for f in os.listdir(input_dir) if f.endswith('.wav')]

    for file_name in input_files:
        # Read the input file
        input_path = os.path.join(input_dir, file_name)
        noise, original_sample_rate = sf.read(input_path)

        # Resample the noise if the sample rate differs
        if original_sample_rate != sample_rate:
            noise = resample(noise, int(len(noise) * sample_rate / original_sample_rate))

        # Create subtle variations for the current file
        base_name = os.path.splitext(file_name)[0]
        for i in range(num_variations):
            variation = noise.copy()

            # Apply extremely subtle random volume scaling (0.5% variation)
            variation *= np.random.uniform(0.995, 1.005)  # More subtle volume scaling

            # Save the variation
            variation_name = f"{base_name}variation{i+1}.wav"
            output_path = os.path.join(output_dir, variation_name)
            sf.write(output_path, variation, sample_rate)
            print(f"Generated extremely subtle variation: {output_path}")

# Parameters
input_directory = "/Users/Eyan Sequeira/Desktop/data1/train/noise1594/noise"  # Replace with your input directory path
output_directory = "/Users/Eyan Sequeira/Desktop/data1/train/aug"
number_of_variations = 3  # Number of variations per file
sampling_rate = 8000  # Fixed sample rate (8 kHz)

# Generate variations for all files
generate_variations(input_directory, output_directory, number_of_variations,sampling_rate)
