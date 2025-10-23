import zipfile
import os

def unzip_data(zip_file_path, destination_dir):
    """
    Unzips a zip file to a specified destination directory.

    Args:
        zip_file_path (str): The path to the zip file.
        destination_dir (str): The path to the destination directory.
    """
    if not os.path.exists(zip_file_path):
        raise FileNotFoundError(f"Zip file not found at: {zip_file_path}")

    try:
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(destination_dir)
            print(f"Successfully extracted {zip_file_path} to {destination_dir}")
    except zipfile.BadZipFile:
        raise ValueError(f"Invalid zip file: {zip_file_path}")
