import os
import numpy as np
import soundfile as sf
import librosa

def calculate_snr_given_residual(clean_audio, residual_noise):
    """
    Calculate SNR for denoised audio given residual noise.
    
    Parameters:
    clean_audio (numpy array): Clean reference audio signal
    residual_noise (numpy array): Residual noise in the denoised audio signal
    
    Returns:
    float: SNR for the denoised audio
    """
    # Calculate power of clean signal and residual noise
    signal_power = np.mean(clean_audio**2)
    residual_noise_power = np.mean(residual_noise**2)
    
    # Calculate SNR
    snr_denoised = 10 * np.log10(signal_power / residual_noise_power)
    return snr_denoised

def resample_audio(audio, original_sr, target_sr):
    """
    Resample audio to match the target sample rate.
    
    Parameters:
    audio (numpy array): Audio signal
    original_sr (int): Original sample rate
    target_sr (int): Target sample rate
    
    Returns:
    numpy array: Resampled audio signal
    """
    if original_sr != target_sr:
        print(f"Resampling from {original_sr} Hz to {target_sr} Hz")
        return librosa.resample(audio, orig_sr=original_sr, target_sr=target_sr)
    return audio


# Define the directory and file paths
audio_dir = "C:/Users/alden/OneDrive/Desktop/major_project/Data_Create/snr/"

# Example file paths
clean_audio_path = os.path.join(audio_dir, "clean.wav")
residual_noise_path = os.path.join(audio_dir, "residual_noise.wav")

# Ensure the files exist
for file_path in [clean_audio_path, residual_noise_path]:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

# Read the audio files
clean_audio, sr_clean = sf.read(clean_audio_path)
residual_noise, sr_residual = sf.read(residual_noise_path)

# Check sample rates and resample if needed
target_sr = sr_clean  # Use the clean audio sample rate as the target
residual_noise = resample_audio(residual_noise, sr_residual, target_sr)

# Update sample rates after resampling
sr_residual = target_sr

# Truncate signals to the shortest length (if they differ)
min_length = min(len(clean_audio), len(residual_noise))
clean_audio = clean_audio[:min_length]
residual_noise = residual_noise[:min_length]

# Calculate the denoised SNR using the provided residual noise
snr_denoised = calculate_snr_given_residual(clean_audio, residual_noise)

# Print the results
print(f"Denoised SNR: {snr_denoised:.2f} dB")
