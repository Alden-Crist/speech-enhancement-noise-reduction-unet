import os
import numpy as np
import soundfile as sf
import librosa
import pystoi  # Install with: pip install pystoi

def calculate_snr(clean_audio, noisy_audio, denoised_audio):
    """
    Calculate SNR for noisy and denoised audio.
    
    Parameters:
    clean_audio (numpy array): Clean reference audio signal
    noisy_audio (numpy array): Noisy input audio signal
    denoised_audio (numpy array): Denoised output audio signal
    
    Returns:
    tuple: SNR for noisy audio, SNR for denoised audio
    """
    # Calculate noise and residual noise
    noise = noisy_audio - clean_audio
    residual_noise = denoised_audio - clean_audio

    # Calculate power of clean signal, noise, and residual noise
    signal_power = np.mean(clean_audio**2)
    noise_power = np.mean(noise**2)
    residual_noise_power = np.mean(residual_noise**2)

    # Calculate SNRs
    snr_noisy = 10 * np.log10(signal_power / noise_power)
    snr_denoised = 10 * np.log10(signal_power / residual_noise_power)

    return snr_noisy, snr_denoised

def calculate_stoi(clean_audio, noisy_audio, denoised_audio, sr):
    """
    Calculate STOI for noisy and denoised audio signals.
    
    Parameters:
    clean_audio (numpy array): Clean reference audio signal
    noisy_audio (numpy array): Noisy input audio signal
    denoised_audio (numpy array): Denoised output audio signal
    sr (int): Sample rate of the audio signals
    
    Returns:
    tuple: STOI for noisy audio, STOI for denoised audio
    """
    # Calculate STOI for noisy and denoised audio
    stoi_noisy = pystoi.stoi(clean_audio, noisy_audio, sr)
    stoi_denoised = pystoi.stoi(clean_audio, denoised_audio, sr)

    return stoi_noisy, stoi_denoised

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

# Verify files in the directory
print("Files in directory:", os.listdir(audio_dir))

# Example file paths
clean_audio_path = os.path.join(audio_dir, "clean.wav")
noisy_audio_path = os.path.join(audio_dir, "noisy.wav")
denoised_audio_path = os.path.join(audio_dir, "denoised.wav")

# Ensure the files exist
for file_path in [clean_audio_path, noisy_audio_path, denoised_audio_path]:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

# Read the audio files
clean_audio, sr_clean = sf.read(clean_audio_path)
noisy_audio, sr_noisy = sf.read(noisy_audio_path)
denoised_audio, sr_denoised = sf.read(denoised_audio_path)

# Check sample rates and resample if needed
target_sr = sr_clean  # Use the clean audio sample rate as the target
noisy_audio = resample_audio(noisy_audio, sr_noisy, target_sr)
denoised_audio = resample_audio(denoised_audio, sr_denoised, target_sr)

# Update sample rates after resampling
sr_noisy = target_sr
sr_denoised = target_sr

# Truncate signals to the shortest length (if they differ)
min_length = min(len(clean_audio), len(noisy_audio), len(denoised_audio))
clean_audio = clean_audio[:min_length]
noisy_audio = noisy_audio[:min_length]
denoised_audio = denoised_audio[:min_length]

# Calculate SNR
snr_noisy, snr_denoised = calculate_snr(clean_audio, noisy_audio, denoised_audio)

# Calculate STOI
stoi_noisy, stoi_denoised = calculate_stoi(clean_audio, noisy_audio, denoised_audio, sr_clean)

# Print the results
print(f"Noisy SNR: {snr_noisy:.2f} dB")
print(f"Denoised SNR: {snr_denoised:.2f} dB")
print(f"Noisy STOI: {stoi_noisy:.2f}")
print(f"Denoised STOI: {stoi_denoised:.2f}")
