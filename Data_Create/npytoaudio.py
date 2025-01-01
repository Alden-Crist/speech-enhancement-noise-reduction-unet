import os
import numpy as np
import librosa
import soundfile as sf


def load_npy_files(magnitude_file, phase_file):
    """
    Load magnitude and phase arrays from .npy files.

    Args:
        magnitude_file (str): Path to the magnitude .npy file.
        phase_file (str): Path to the phase .npy file.

    Returns:
        magnitude (np.ndarray): The magnitude array.
        phase (np.ndarray): The phase array.
    """
    magnitude = np.load(magnitude_file)
    phase = np.load(phase_file)
    return magnitude, phase


def reconstruct_audio(magnitude, phase, n_fft, hop_length_fft):
    """
    Reconstruct audio from magnitude and phase arrays using ISTFT.

    Args:
        magnitude (np.ndarray): Magnitude array.
        phase (np.ndarray): Phase array.
        n_fft (int): FFT window size.
        hop_length_fft (int): Hop length for FFT.

    Returns:
        audio (np.ndarray): Reconstructed audio signal.
    """
    # Convert magnitude to linear scale
    magnitude_linear = librosa.db_to_amplitude(magnitude)
    
    # Check if the size of magnitude is smaller than n_fft and adjust n_fft if needed
    if magnitude.shape[0] < n_fft:
        print(f"Warning: Adjusting n_fft from {n_fft} to {magnitude.shape[0]} due to smaller frame size.")
        n_fft = magnitude.shape[0]
    
    # Combine magnitude and phase
    stft_matrix = magnitude_linear * np.exp(1j * phase)
    
    # Reconstruct the audio signal
    audio = librosa.istft(stft_matrix, hop_length=hop_length_fft, win_length=n_fft)
    return audio


def save_audio(audio, output_path, sample_rate):
    """
    Save the reconstructed audio to a file.

    Args:
        audio (np.ndarray): The audio signal.
        output_path (str): Path to save the audio file.
        sample_rate (int): Sample rate for the audio file.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    sf.write(output_path, audio, sample_rate)


if __name__ == "__main__":
    magnitude_file = "./npy/noisy_voice_amp_db_batch_0.npy"
    phase_file = "./npy/noisy_voice_pha_db_batch_0.npy"
    output_folder = "./output/"

    # Parameters based on your setup
    sample_rate = 8000
    n_fft = 255  # Keep this as default
    hop_length_fft = 63

    # Load and check data dimensions
    magnitude, phase = load_npy_files(magnitude_file, phase_file)
    print("Magnitude shape:", magnitude.shape)
    print("Phase shape:", phase.shape)

    # Process each segment and save as individual audio files
    for i in range(magnitude.shape[0]):
        print(f"Processing segment {i + 1}/{magnitude.shape[0]}...")
        try:
            audio = reconstruct_audio(magnitude[i], phase[i], n_fft, hop_length_fft)
            output_audio_path = os.path.join(output_folder, f"output_audio_{i}.wav")
            save_audio(audio, output_audio_path, sample_rate)
            print(f"Audio segment {i} saved to {output_audio_path}")
        except Exception as e:
            print(f"Error processing segment {i}: {e}")
