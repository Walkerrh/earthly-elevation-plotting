import os
import re
import rasterio
import matplotlib.pyplot as plt

def parse_filename_to_coords(filename):
    match = re.match(r"(\d+)_DEM_y(-?\d+)x(-?\d+)\.tif", filename)
    if match:
        return match.group(2), match.group(3)  # Return latitude, longitude
    else:
        return None

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

def get_existing_visualizations(save_dir):
    existing_files = set()
    for filename in os.listdir(save_dir):
        if filename.endswith('.png'):
            existing_files.add(filename.rsplit('.', 1)[0])
    return existing_files

def main():
    save_directory = "/Volumes/Extreme SSD/topg_europa/save_img"
    tif_directory = "/Volumes/Extreme SSD/topg_europa/tif"
    
    existing_visualizations = get_existing_visualizations(save_directory)
    processed_count = 0

    # Iterate over every .tif file in the tif_directory
    for filename in os.listdir(tif_directory):
        if filename.endswith('.tif'):
            coords = parse_filename_to_coords(filename)
            if coords:
                y_coord, x_coord = coords
                visualization_name = f'y{y_coord}x{x_coord}'
                if visualization_name not in existing_visualizations:
                    file_path = os.path.join(tif_directory, filename)
                    try:
                        save_visualization_with_coords(file_path, save_directory, y_coord, x_coord)
                        processed_count += 1
                    except Exception as e:
                        print(f"An error occurred while processing {filename}: {e}")
    
    print(f"Processed {processed_count} files.")
    print(f"Existing visualizations: {len(existing_visualizations)}")
    print(f"Total .tif files: {len([name for name in os.listdir(tif_directory) if name.endswith('.tif')])}")

if __name__ == "__main__":
    main()
