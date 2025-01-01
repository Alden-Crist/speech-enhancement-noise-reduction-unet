import os
import random
from pydub import AudioSegment

# Path to the directory containing your noise files
directory = '/Users/alden/OneDrive/Desktop/Data/Train/noise1600'

# Path to the folder where mixed files will be saved
output_directory = '/Users/alden/OneDrive/Desktop/Data/Train/aug1600_mixed'

# Ensure output directory exists, if not, create it
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Get all the noise file names from the directory
noise_files = [f for f in os.listdir(directory) if f.endswith('.wav')]

# Function to get the noise type (last two digits of the filename)
def get_noise_type(filename):
    return int(filename.split('-')[-1].split('.')[0])

# Function to mix two audio files
def mix_files(file1, file2, output_filename):
    # Load the two files
    sound1 = AudioSegment.from_file(file1)
    sound2 = AudioSegment.from_file(file2)

    # Ensure both files have the same length (repeat the shorter one)
    if len(sound1) > len(sound2):
        sound2 = sound2 * (len(sound1) // len(sound2)) + sound2[:len(sound1) % len(sound2)]
    elif len(sound2) > len(sound1):
        sound1 = sound1 * (len(sound2) // len(sound1)) + sound1[:len(sound2) % len(sound1)]

    # Mix the two sounds by overlaying one on top of the other (simple addition)
    mixed_sound = sound1 + sound2

    # Export the mixed file
    mixed_sound.export(output_filename, format="wav")
    print(f"Created mixed file: {output_filename}")

# Iterate over each noise file in the directory
for file in noise_files:
    # Get the noise type (last two digits of the file name)
    noise_type = get_noise_type(file)
    
    # Randomly select two other noise files to mix (avoid mixing with itself)
    possible_files = [f for f in noise_files if get_noise_type(f) != noise_type]
    random_files = random.sample(possible_files, 2)

    # Construct full file paths
    file_path = os.path.join(directory, file)
    file1_path = os.path.join(directory, random_files[0])
    file2_path = os.path.join(directory, random_files[1])

    # Generate the mixed filenames in the output directory
    mixed_file1 = os.path.join(output_directory, f"mixed_{noise_type}_{get_noise_type(random_files[0])}_{get_noise_type(random_files[1])}_1.wav")
    mixed_file2 = os.path.join(output_directory, f"mixed_{noise_type}_{get_noise_type(random_files[0])}_{get_noise_type(random_files[1])}_2.wav")

    # Mix the noise files and save them
    mix_files(file_path, file1_path, mixed_file1)
    mix_files(file_path, file2_path, mixed_file2)
