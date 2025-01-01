import os
from data_tools import audio_files_to_numpy
from data_tools import blend_noise_randomly, numpy_audio_to_matrix_spectrogram
import numpy as np
import soundfile as sf


def create_data(noise_dir, voice_dir, path_save_time_serie, path_save_sound, path_save_spectrogram, sample_rate,
                min_duration, frame_length, hop_length_frame, hop_length_frame_noise, nb_samples, n_fft, hop_length_fft):
    """This function will randomly blend some clean voices from voice_dir with some noises from noise_dir
    and save the spectrograms of noisy voice, noise and clean voices to disk as well as complex phase,
    time series and sounds. This aims at preparing datasets for denoising training. It takes as inputs
    parameters defined in args module"""

    list_voice_files = os.listdir(voice_dir)
    list_noise_files = os.listdir(noise_dir)

    def remove_ds_store(lst):
        """remove mac specific file if present"""
        if '.DS_Store' in lst:
            lst.remove('.DS_Store')
        return lst

    list_voice_files = remove_ds_store(list_voice_files)
    list_noise_files = remove_ds_store(list_noise_files)


    nb_voice_files = len(list_voice_files)
    nb_noise_files = len(list_noise_files)

    
    print(nb_voice_files)
    print(nb_noise_files)

    noise = audio_files_to_numpy(noise_dir, list_noise_files, sample_rate,
                                 frame_length, hop_length_frame_noise, min_duration)
    voice = audio_files_to_numpy(voice_dir, list_voice_files,
                                 sample_rate, frame_length, hop_length_frame, min_duration)

    prod_voice, prod_noise, prod_noisy_voice = blend_noise_randomly(
        voice, noise, nb_samples, frame_length)

    # Reshape long audio arrays to save to disk
    if prod_voice is None or prod_noise is None or prod_noisy_voice is None:
        print("Blending failed due to empty input arrays. Check your audio data.")
    else:
        noisy_voice_long = prod_noisy_voice.reshape(1, nb_samples * frame_length)
        voice_long = prod_voice.reshape(1, nb_samples * frame_length)
        noise_long = prod_noise.reshape(1, nb_samples * frame_length)

        sf.write(path_save_sound + 'noisy_voice_long.wav', noisy_voice_long[0, :], sample_rate)
        sf.write(path_save_sound + 'voice_long.wav', voice_long[0, :], sample_rate)
        sf.write(path_save_sound + 'noise_long.wav', noise_long[0, :], sample_rate)

        dim_square_spec = int(n_fft / 2) + 1

        batch_size = 1000  # Adjust this based on available memory
        for i in range(0, nb_samples, batch_size):
            batch_voice = prod_voice[i:i+batch_size]
            batch_noise = prod_noise[i:i+batch_size]
            batch_noisy_voice = prod_noisy_voice[i:i+batch_size]

            # Convert each batch to spectrogram
            m_amp_db_voice, m_pha_voice = numpy_audio_to_matrix_spectrogram(
                batch_voice, dim_square_spec, n_fft, hop_length_fft)
            m_amp_db_noise, m_pha_noise = numpy_audio_to_matrix_spectrogram(
                batch_noise, dim_square_spec, n_fft, hop_length_fft)
            m_amp_db_noisy_voice, m_pha_noisy_voice = numpy_audio_to_matrix_spectrogram(
                batch_noisy_voice, dim_square_spec, n_fft, hop_length_fft)

            # Save each batch to disk
            np.save(path_save_time_serie + f'voice_timeserie_batch_{i}', batch_voice)
            np.save(path_save_time_serie + f'noise_timeserie_batch_{i}', batch_noise)
            np.save(path_save_time_serie + f'noisy_voice_timeserie_batch_{i}', batch_noisy_voice)

            np.save(path_save_spectrogram + f'voice_amp_db_batch_{i}', m_amp_db_voice)
            np.save(path_save_spectrogram + f'noise_amp_db_batch_{i}', m_amp_db_noise)
            np.save(path_save_spectrogram + f'noisy_voice_amp_db_batch_{i}', m_amp_db_noisy_voice)

            np.save(path_save_spectrogram + f'voice_pha_db_batch_{i}', m_pha_voice)
            np.save(path_save_spectrogram + f'noise_pha_db_batch_{i}', m_pha_noise)
            np.save(path_save_spectrogram + f'noisy_voice_pha_db_batch_{i}', m_pha_noisy_voice)

