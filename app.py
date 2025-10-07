import os
import shutil
import time

# Set the directory to be cleaned
DOWNLOADS_DIR = os.path.expanduser("~/Downloads")
DESTINATION_BASE_DIR = os.path.join(DOWNLOADS_DIR, "Cleaned Files")
LOG_FILE_PATH = os.path.join(DESTINATION_BASE_DIR, "_Log.txt")

# Define the folder structure and file extensions
FILE_TYPE_MAPPING = {
    "Documents": ['.doc', '.docx', '.pdf', '.rtf', '.wpd', '.txt', '.wps', '.msg', '.md', '.yml', '.tf', '.Dockerfile', '.ppt', '.pptx', '.gslides', '.key', '.odp', '.csv', '.xls', '.xlsx'],
    "Media/Images": ['.png', '.jpg', '.jpeg', '.gif', '.heif', '.svg', '.webp', '.tif', '.bmp', '.eps'],
    "Media/Videos": ['.amv', '.mpeg', '.flv', '.avi', '.mp4', '.3gp', '.mov', '.wmv'],
    "Media/Audio": ['.aac', '.mp3', '.wav', '.wma', '.snd', '.ra', '.au'],
    "Development": ['.c', '.py', '.java', '.js', '.cpp', '.ts', '.cs', '.swift', '.pl', '.bat', '.sh'],
    "Installers": ['.com', '.exe', '.iso', '.msi'],
    "Web": ['.htm', '.html', '.xhtml', '.aspx', '.asp', '.css', '.xps', '.rss'],
    "Archives": ['.rar', '.tar', '.7z', '.zip', '.hgx', '.arj', '.arc', '.sit', '.gz', '.z'],
    "Data": ['.xml', '.json', '.sql', '.dta'],
    "Other": []  # For files that don't match any other category
}

def create_destination_folders():
    """Creates the destination folders if they don't exist."""
    for folder in FILE_TYPE_MAPPING.keys():
        os.makedirs(os.path.join(DESTINATION_BASE_DIR, folder), exist_ok=True)
    os.makedirs(os.path.join(DESTINATION_BASE_DIR, "Other"), exist_ok=True)

def get_destination_folder(file_extension):
    """Returns the destination folder for a given file extension."""
    for folder, extensions in FILE_TYPE_MAPPING.items():
        if file_extension.lower() in extensions:
            return os.path.join(DESTINATION_BASE_DIR, folder)
    return os.path.join(DESTINATION_BASE_DIR, "Other")

def clean_folder():
    """Organizes files in the Downloads folder."""
    with open(LOG_FILE_PATH, 'a+') as log_file:
        log_file.write(f"Script started at: {time.ctime()}\n")
        for root, _, files in os.walk(DOWNLOADS_DIR):
            # Skip the destination directory itself
            if os.path.commonpath([root, DESTINATION_BASE_DIR]) == DESTINATION_BASE_DIR:
                continue

            for file in files:
                source_path = os.path.join(root, file)

                # Skip the log file itself
                if source_path == LOG_FILE_PATH:
                    continue

                _, file_extension = os.path.splitext(file)
                destination_folder = get_destination_folder(file_extension)
                destination_path = os.path.join(destination_folder, file)

                # Check if the destination path already exists
                if os.path.exists(destination_path):
                    log_file.write(f"Skipped (already exists): {source_path}\n")
                    continue

                try:
                    shutil.move(source_path, destination_path)
                    log_file.write(f"Moved: {source_path} -> {destination_path}\n")
                except OSError as e:
                    if e.winerror == 32:  # File is in use
                        log_file.write(f"Skipped (file in use): {source_path}\n")
                    else:
                        log_file.write(f"Error moving {source_path}: {e}\n")
                except Exception as e:
                    log_file.write(f"Error moving {source_path}: {e}\n")
        log_file.write(f"Script finished at: {time.ctime()}\n\n")

if __name__ == "__main__":
    create_destination_folders()
    clean_folder()
    print(f"Folder cleaning complete. See {LOG_FILE_PATH} for details.")