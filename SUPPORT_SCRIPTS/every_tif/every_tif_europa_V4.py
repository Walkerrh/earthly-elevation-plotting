import os
import re
import rasterio

from rasterio.mask import mask
import earthpy.plot as ep
import earthpy.spatial as es

import matplotlib.pyplot as plt

def parse_filename_to_coords(filename):
    match = re.match(r"(\d+)_DEM_y(-?\d+)x(-?\d+)\.tif", filename)
    if match:
        return match.group(2), match.group(3)  # Return latitude, longitude
    else:
        raise ValueError("Filename does not match expected format")

def save_hillshade_image(file_path, save_dir, y_coord, x_coord):

    bbox = box( # need to change to to the relative size of the passed .tif file
        minx=700, 
        miny=1000, 
        maxx=900, 
        maxy=1200
        ) #xmin, ymin, xmax, ymax
    
    with rasterio.open(file_path) as src:
        out_image, out_transform = mask(src, [bbox])
        # data = src.read(1)  # read the first band
        
        # Generate hillshade from the DEM
        hillshade = es.hillshade(out_image, azimuth=30, altitude=30)
        
        # Plot the hillshade
        # ep.plot_bands(
        #     hillshade,
        #     cmap='gray',
        #     cbar=False,
        #     title=f'Hillshade LATITUDE(Y):{y_coord} LONGITUDE(X):{x_coord}'
        # )
        
        ep.colorbar(hillshade, 'gray')
        ep.title(hillshade, f'LATITUDE(Y):{y_coord} LONGITUDE(X):{x_coord}')
        
        # Create filename with y and x coordinates
        output_path = os.path.join(save_dir, f'y{y_coord}x{x_coord}_hillshade.png')
        
        # Save the figure to a file
        plt.savefig(output_path, bbox_inches='tight', pad_inches=0)
        plt.close()  # Close the figure to avoid displaying it
    print(f"Saved hillshade image for {file_path} as {output_path}")

def process_tif_files(tif_directory, save_directory, start_index=0):
    tif_files = [f for f in os.listdir(tif_directory) if f.endswith('.tif') and not f.startswith('._')]
    tif_files.sort()  # Sort the files to process them in order

    for index, filename in enumerate(tif_files, start=1):
        if index >= start_index:
            print(f"Processing file {index} in line: {filename}")
            try:
                coords = parse_filename_to_coords(filename)
                y_coord, x_coord = coords
                file_path = os.path.join(tif_directory, filename)
                save_hillshade_image(file_path, save_directory, y_coord, x_coord)
            except ValueError as e:
                print(f"Skipping file {filename}: {e}")
            except Exception as e:
                print(f"An error occurred while processing {filename}: {e}")

def main():
    save_directory = "/Volumes/Extreme SSD/topg_europa/save_img_earthpy"
    tif_directory = "/Volumes/Extreme SSD/topg_europa/tif"
    start_at = 1  # Change this number to start processing from a specific file index

    process_tif_files(tif_directory, save_directory, start_at)

if __name__ == "__main__":
    main()
