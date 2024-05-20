
""" 
The structure of the code is made to run on a file format of:

            TOP_FOLDER
            |        |
    europa_folder   tif_folder
        |                |
    FOLDERS         (nothing)
    |
  .tif_files
            
for every folder in FOLDERS:
    look for .tif files
        move .tif file to tif_folder
"""

import os
import shutil

def move_tif_files(base_dir):
    # Define the paths for "europa" and "tif" directories
    europa_dir = os.path.join(base_dir, "europa")
    tif_dir = os.path.join(base_dir, "tif")

    # Check if the base directory, "europa", and "tif" directories exist
    if not os.path.exists(base_dir):
        print("The provided directory path does not exist.")
        return

    if not os.path.exists(europa_dir) or not os.path.exists(tif_dir):
        print("The 'europa' and/or 'tif' folders do not exist in the provided directory.")
        return

    # Loop through each folder inside "europa"
    for subdir in os.listdir(europa_dir):
        subdir_path = os.path.join(europa_dir, subdir)
        
        # Ensure it's a directory
        if os.path.isdir(subdir_path):
            # For each file in the current subdir of "europa"
            for filename in os.listdir(subdir_path):
                if filename.endswith(".tif") and not filename.startswith("._"):
                    file_path = os.path.join(subdir_path, filename)
                    destination_path = os.path.join(tif_dir, filename)

                    # Move the .tif file to the "tif" directory
                    shutil.move(file_path, destination_path)

    print("Operation completed!")

if __name__ == "__main__":
    directory_path = input("Enter the path to the directory: ")
    move_tif_files(directory_path)