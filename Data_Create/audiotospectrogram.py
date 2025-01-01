import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt

# Load an audio file (Windows path)
audio_path = r'C:\Users\alden\OneDrive\Desktop\majorproject junk\audio\example_audio.wav'  # Add the full filename
y, sr = librosa.load(audio_path)

# Create a Mel spectrogram
S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000)  # Mel spectrogram with 128 bands
S_db = librosa.power_to_db(S, ref=np.max)  # Convert power spectrogram to dB scale

# Plot the Mel spectrogram
plt.figure(figsize=(12, 6))  # Adjust the size for better visibility
librosa.display.specshow(S_db, sr=sr, x_axis='time', y_axis='mel')  # Use 'mel' for Mel scale on y-axis
plt.colorbar(format='%+2.0f dB')
plt.title('Mel Spectrogram')
plt.xlabel('Time (s)')
plt.ylabel('Frequency (Hz)')
plt.tight_layout()
plt.show()
