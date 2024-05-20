import os
import re
import rasterio
import matplotlib.pyplot as plt

def parse_filename_to_coords(filename):
    match = re.match(r"(\d+)_DEM_y(-?\d+)x(-?\d+)\.tif", filename)
    if match:
        return match.group(2), match.group(3)  # Return latitude, longitude
    else:
        raise ValueError("Filename does not match expected format")

def save_visualization_with_coords(file_path, save_dir, y_coord, x_coord):
    with rasterio.open(file_path) as file:
        data = file.read(1)  # read the first band
        plt.imshow(data, cmap='terrain')
        plt.colorbar()
        plt.title(f'LATITUDE(Y):{y_coord} LONGITUDE(X):{x_coord}')
        
        # Create filename with y and x coordinates
        output_path = os.path.join(save_dir, f'y{y_coord}x{x_coord}.png')
        plt.savefig(output_path)
        plt.close()  # Close the figure to avoid displaying it
    print(f"Saved visualization for {file_path} as {output_path}")

def process_tif_files(tif_directory, save_directory, start_index=0, stop_index=None):
    tif_files = [f for f in os.listdir(tif_directory) if f.endswith('.tif') and not f.startswith('._')]
    tif_files.sort()  # Sort the files to process them in order

    for index, filename in enumerate(tif_files, start=1):
        if index >= start_index:
            if stop_index is not None and index > stop_index:
                print(f"Reached stopping point at file {index} in line. Exiting.")
                break  # Exit the loop if the current index exceeds the stop_index
            print(f"Processing file {index} in line: {filename}")
            try:
                coords = parse_filename_to_coords(filename)
                y_coord, x_coord = coords
                file_path = os.path.join(tif_directory, filename)
                save_visualization_with_coords(file_path, save_directory, y_coord, x_coord)
            except ValueError as e:
                print(f"Skipping file {filename}: {e}")
            except Exception as e:
                print(f"An error occurred while processing {filename}: {e}")

def main():
    save_directory = "/Volumes/Extreme SSD/topg_europa/save_img"
    tif_directory = "/Volumes/Extreme SSD/topg_europa/tif"
    start_at = 336  # Change this to the number to start processing from
    stop_at = 339  # Change this to the number to stop processing after

    process_tif_files(tif_directory, save_directory, start_index=start_at, stop_index=stop_at)

if __name__ == "__main__":
    main()
