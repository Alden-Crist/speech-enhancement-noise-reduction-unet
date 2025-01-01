# Data config =======

UPLOAD_FOLDER   = './uploads/'
SAVE_FOLDER   =   './outputs/'
SPEC_FOLDER  = './spectrograms/'


SUPPORT_FORMAT  = ['mp3', 'mp4', 'wav']

NOISE_DOMAINS   = ['vacuum_cleaner', 'clapping','train','wind','snoring','glass-breaking','car-horn' 
                    'clock_alarm', 'wind', 'keyboard_typing',  'car_horn' , 'church bells', 
                    'breathing',  'clock_tick',  'rain']


# Speech config =====
SAMPLE_RATE         = 8000
N_FFT               = 255
HOP_LENGTH_FFT      = 63
HOP_LENGTH_FRAME    = 8064
FRAME_LENGTH        = 8064
MIN_DURATION        = 1.0