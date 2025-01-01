import os

def delete_files_by_class(directory, class_list):
    """
    Deletes files from the given directory where the last two digits of the filename 
    (before the '.wav' extension) match any entry in the provided class_list.
    
    :param directory: Directory where the files are located.
    :param class_list: List of classes (numbers) to delete from the filenames.
    """
    # Loop through each file in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".wav"):
            # Extract the last two digits (class) before the '.wav' extension
            file_class = filename.split('-')[-1].split('.')[0]
            
            # If the class is in the class_list, delete the file
            if file_class in class_list:
                file_path = os.path.join(directory, filename)
                try:
                    os.remove(file_path)
                    print(f"Deleted: {filename}")
                except Exception as e:
                    print(f"Error deleting {filename}: {e}")

# Example usage
directory = '/Users/alden/OneDrive/Desktop/Data/Train/noise359' # Replace with the actual directory path
class_list = ['26', '43']  # List of classes you want to delete

delete_files_by_class(directory, class_list)
