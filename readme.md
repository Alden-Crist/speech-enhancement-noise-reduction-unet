Here’s a rephrased version of the README.md:

---

# Speech Enhancement Using Deep Learning

## Project Overview

This project focuses on developing a speech enhancement system to reduce environmental noise using deep learning techniques.

## Spectrogram Denoising

Audio can be represented in several forms, ranging from raw time-series to time-frequency decompositions. For optimal performance, the choice of representation is crucial. Among the various methods, spectrograms are highly effective for audio processing. A spectrogram is a 2D image that represents the Short-Time Fourier Transform (STFT) with time and frequency axes, where brightness indicates the intensity of each frequency component at specific time frames. Spectrograms are ideal for applying Convolutional Neural Networks (CNNs) due to their image-like structure.

For this project, I used magnitude spectrograms to represent the audio. The goal is to predict and subtract the noise from a noisy speech spectrogram.

## Project Structure

The project is divided into three main phases: data creation, model training, and prediction.

### Data Preparation

The data required for training was sourced from various places. Clean English speech data was obtained from the LibriSpeech dataset, while environmental noise data was gathered from the ESC-50 dataset and other publicly available sources.

The environmental noise data covers 10 types of noise: tic clock, footsteps, bells, handsaw, alarm, fireworks, insects, brushing teeth, vacuum cleaner, and snoring.

To build the training and validation datasets, the audio files were sampled at 8 kHz, and 1-second-long audio windows were extracted. Data augmentation was applied to the noise data by selecting windows from various points in the recordings. The clean voice and noise samples were mixed with varying noise levels (ranging from 20% to 80%).

The final training dataset consists of 10 hours of noisy and clean voice samples, and the validation dataset includes 1 hour of audio.

To prepare the data:
1. Create directories for training and testing data, separate from the project folder.
2. Place the clean voice files in the `voice_dir` and the noise audio files in the `noise_dir`.
3. Modify the path variables in the `args.py` file to point to these directories.
4. Run the data creation script: `python main.py --mode='data_creation'`.

This will randomly combine clean voices and noise samples, then generate spectrograms for both noisy and clean voices.

### Model Training

For training, a U-Net architecture is employed, which is a type of deep convolutional autoencoder. The U-Net model was originally designed for medical image segmentation but is adapted here for denoising spectrograms.

The model receives magnitude spectrograms of noisy voices as input and outputs the noise model, which is subtracted from the noisy spectrogram to obtain the clean voice spectrogram. The training data consists of noisy voice spectrograms and their corresponding clean voice spectrograms.

The encoder of the U-Net consists of 10 convolutional layers with LeakyReLU activations, max-pooling, and dropout. The decoder is symmetric with skip connections. The output layer uses the hyperbolic tangent (tanh) activation function to scale the output between -1 and 1. The model is compiled with the Adam optimizer and uses Huber loss, which balances between L1 and L2 loss.

Training typically takes several hours on a modern GPU. To train the model, run:
```bash
python main.py --mode="training"
```

### Prediction

For prediction, noisy audio files are processed into time series and converted into spectrograms. These spectrograms are then passed through the trained U-Net model to predict the noise model. The predicted noise is subtracted from the noisy voice spectrogram, and the result is combined with the original phase spectrogram to reconstruct the clean audio.

### Results

The model was evaluated on validation data consisting of noisy audio examples from various noise types (alarm, insects, vacuum cleaner, bells). The network successfully generalized the noise removal process and produced denoised spectrograms that closely matched the clean voice spectrograms.

Additionally, the denoising process was tested on audio with high noise levels, and the model performed well, significantly improving audio quality.

### How to Use

1. Clone this repository.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the program with different modes:
   ```bash
   python main.py --mode [data_creation | training | prediction]
   ```

For more detailed configuration options, check the `args.py` file.

