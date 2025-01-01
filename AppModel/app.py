import os
import requests
from PIL import Image
import streamlit as st
from utils.app_utils import prediction, analyst_result, play_file_uploaded, process_input_format
from config import *
import moviepy.editor as mp

# Move st.set_page_config to the top before any other Streamlit commands
st.set_page_config(
    page_title="Speech Enhancement",
    page_icon="📢",
    layout="wide",
    initial_sidebar_state="collapsed",
)

@st.cache_data  # Removed the allow_output_mutation argument
def load_session():
    return requests.Session()

def save_uploadedfile(uploadedfile, file_type):
    filename = uploadedfile.name

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    with open(os.path.join(UPLOAD_FOLDER, uploadedfile.name), "wb") as f:
        f.write(uploadedfile.getbuffer())
    
    process_input_format(filename, file_type)

def main():
    st.title(':musical_note: Speech Enhancement')
    st.subheader('Remove your audio background noise')

    sess = load_session()

    uploaded_file = st.file_uploader("🎤Upload your audio/video:", type=SUPPORT_FORMAT)

    file_type = ''
    file_name = ''
    file_format = ''

    # Play uploaded file
    if uploaded_file is not None:
        st.subheader('Input audio/video')

        file_type = uploaded_file.type
        file_name = uploaded_file.name
        file_format = file_name[-3:]

        if file_format not in SUPPORT_FORMAT:
            st.error('We do not support this format yet!')
        else:
            play_file_uploaded(uploaded_file, file_type)

    # Use st.columns instead of st.beta_columns
    col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11 = st.columns([1,1,1,1,1,1,1,1,1,1,1])
    
    is_success = False

    if uploaded_file is not None and col6.button('Start reducing!'):
        save_uploadedfile(uploaded_file, file_type)

        m_amp_db, m_pha, pred_amp_db, X_denoise = prediction(
                    weights_path="./Model",
                    name_model="model_unet40000",
                    audio_dir_prediction=UPLOAD_FOLDER,
                    dir_save_prediction=SAVE_FOLDER,
                    audio_input_prediction=[file_name[:-3] + 'wav'],
                    audio_output_prediction="out_" + file_name[:-3] + 'wav',
                    sample_rate=SAMPLE_RATE,
                    min_duration=MIN_DURATION,
                    frame_length=FRAME_LENGTH,
                    hop_length_frame=HOP_LENGTH_FRAME,
                    n_fft=N_FFT,
                    hop_length_fft=HOP_LENGTH_FFT
        )


        analyst_result(file_name[:-3] + 'wav', m_amp_db, m_pha, pred_amp_db, X_denoise)
        is_success = True

    if is_success:
        if 'audio' in uploaded_file.type:
            out_wav = file_name[:-3] + 'wav'
            out_audio_file = open(os.path.join(SAVE_FOLDER, f'out_{out_wav}'), 'rb')
            out_audio_bytes = out_audio_file.read()
            st.header(':musical_note: Your processed audio/video')
            st.audio(out_audio_bytes, format='audio/wav')

        elif 'video' in uploaded_file.type:
            origin_vid = mp.VideoFileClip(os.path.join(UPLOAD_FOLDER, file_name))
            processed_audio = mp.AudioFileClip(os.path.join(SAVE_FOLDER, f'out_{file_name[:-4]}.wav'))
            processed_vid = origin_vid.set_audio(processed_audio)
            processed_vid.write_videofile(SAVE_FOLDER + f'out_{file_name[:-4]}.mp4')

            out_audio_file = open(os.path.join(SAVE_FOLDER, f'out_{file_name[:-4]}.mp4'), 'rb')
            out_audio_bytes = out_audio_file.read()
            st.header(':musical_note: Your processed audio/video')
            st.video(out_audio_bytes, format='video/mp4')

        st.subheader('Advanced details')

        # Use st.expander instead of st.beta_expander
        my_expander1 = st.expander('Noisy speech')
        with my_expander1:
            st.subheader('Input detail')
            col1, col2 = st.columns([1,1])
            noisy_spec = Image.open(os.path.join(SPEC_FOLDER, 'noisy_spec.png'))
            noisy_time_serie = Image.open(os.path.join(SPEC_FOLDER, 'noisy_time_serie.png'))
            col1.image(noisy_time_serie)
            col2.image(noisy_spec)

        my_expander2 = st.expander('Noise detail')
        with my_expander2:
            st.subheader('Noise prediction')
            col1, col2 = st.columns([1,1])
            noise_spec = Image.open(os.path.join(SPEC_FOLDER, 'noise_spec.png'))
            col2.image(noise_spec)
            
        my_expander3 = st.expander('Output detail')
        with my_expander3:
            st.subheader('Clean noise speech')
            col1, col2 = st.columns([1,1])
            out_spec = Image.open(os.path.join(SPEC_FOLDER, 'out_spec.png'))
            out_time_serie = Image.open(os.path.join(SPEC_FOLDER, 'out_time_serie.png'))
            col1.image(out_time_serie)
            col2.image(out_spec)

if __name__ == '__main__':
    main()

