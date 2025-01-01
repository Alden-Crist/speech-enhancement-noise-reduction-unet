import os
from pydub import AudioSegment

def mix_background_noise(voice_folder, noise_folder, output_folder, noise_ratio=0.1):
    """
    Mixes background noise into clean voice audio files from specified folders.

    Parameters:
        voice_folder (str): Path to the folder containing clean voice audio files.
        noise_folder (str): Path to the folder containing background noise audio files.
        output_folder (str): Path to the folder where mixed audio files will be saved.
        noise_ratio (float): Ratio of noise in the final output (0 to 1).

    Returns:
        None
    """
    # Get the list of voice and noise files
    voice_files = [f for f in os.listdir(voice_folder) if f.endswith(".wav")]
    noise_files = [f for f in os.listdir(noise_folder) if f.endswith(".wav")]

    if not voice_files:
        print("No voice files found in the voice folder.")
        return
    if not noise_files:
        print("No noise files found in the noise folder.")
        return

    # Use the first noise file for simplicity
    noise_path = os.path.join(noise_folder, noise_files[0])
    noise = AudioSegment.from_file(noise_path)

    # Process each voice file
    for voice_file in voice_files:
        voice_path = os.path.join(voice_folder, voice_file)
        voice = AudioSegment.from_file(voice_path)

        # Adjust the length of the noise to match the voice
        if len(noise) < len(voice):
            noise = noise * (len(voice) // len(noise) + 1)
        noise = noise[:len(voice)]

        # Calculate the dynamic reduction of noise volume
        voice_db = voice.dBFS  # Average volume of the voice in dBFS
        noise_db = noise.dBFS  # Average volume of the noise in dBFS

        # Reduce noise volume to always be significantly quieter than the voice
        adjusted_noise_db = voice_db - 15 * (1 - noise_ratio)  # More aggressive reduction
        noise_gain = adjusted_noise_db - noise_db  # Gain adjustment for noise
        adjusted_noise = noise + noise_gain

        # Mix the two audio files
        mixed_audio = voice.overlay(adjusted_noise)

        # Save the output
        output_file = os.path.join(output_folder, f"mixed_{voice_file}")
        mixed_audio.export(output_file, format="wav")
        print(f"Mixed audio saved to: {output_file}")

# Directory paths
voice_folder = "C:/Users/alden/OneDrive/Desktop/major_project/Data_Create/voice/"
noise_folder = "C:/Users/alden/OneDrive/Desktop/major_project/Data_Create/noise/"
output_folder = "C:/Users/alden/OneDrive/Desktop/major_project/Data_Create/output/"

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Mix background noise with clean voice
mix_background_noise(voice_folder, noise_folder, output_folder, noise_ratio=0.05)
