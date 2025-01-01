Data Preparation:

The clean voice data is sourced from the LibriSpeech corpus and SiSec, while environmental noise data is from the ESC-50 dataset and other sound repositories.
Data augmentation is applied to the noise by selecting different time windows, and clean voices are blended with various levels of noise (20%-80%).
The audio data is converted to spectrograms using Short-Time Fourier Transform (STFT), with a default size of 128x128 for each spectrogram.

Training:

A U-Net model is trained to predict the noise model (difference between noisy and clean spectrograms) using magnitude spectrograms of noisy and clean voices.
The network architecture includes 10 convolutional layers in the encoder, with a symmetric decoder path and skip connections.
The model is trained with the Adam optimizer and Huber loss, and weights are saved as the best model during training.

Prediction:

For predictions, noisy audio is converted into time series, which are then transformed into magnitude spectrograms.
The U-Net model predicts the noise, which is subtracted from the noisy spectrogram to produce a denoised output. The denoised spectrogram is combined with the original phase information and converted back into audio.
The project is designed to work efficiently on a GPU, and results show that the network can generalize well, producing denoised spectrograms close to the true clean voice spectrograms.