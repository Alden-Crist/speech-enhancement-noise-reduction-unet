from pydub import AudioSegment
import os

# Define paths for input and output folders
voice_dir = "/Users/alden/OneDrive/Desktop/Data/Train/clean_voice"
output_folder = "/Users/alden/OneDrive/Desktop/Data/Train/clean_voice/converted_wav_files"

# Create the directory if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Function to list all FLAC files in a directory
def list_flac_files(directory):
    flac_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.flac'):
                flac_files.append(os.path.join(root, file))  # Get full path
    return flac_files

# Get the list of FLAC files to be converted
list_voice_files = list_flac_files(voice_dir)

# Function to convert a single FLAC file to WAV
def convert_flac_to_wav(flac_path, output_folder):
    # Define the output path for the WAV file
    wav_path = os.path.join(output_folder, os.path.basename(flac_path).replace(".flac", ".wav"))

    # Convert and save the file
    audio = AudioSegment.from_file(flac_path, format="flac")
    audio.export(wav_path, format="wav")

# Convert all FLAC files in the list
for flac_file in list_voice_files:
    convert_flac_to_wav(flac_file, output_folder)

print("Conversion complete. WAV files saved in:", output_folder)
