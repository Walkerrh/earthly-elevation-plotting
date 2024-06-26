


import os
import re
import random
import requests
import rasterio
import matplotlib.pyplot as plt

def generate_random_ip():
    return ".".join(str(random.randint(0, 255)) for _ in range(4))

def ip_to_latlong(ip_address):
    # Query the ipinfo.io API for geolocation data of the IP
    response = requests.get(f"https://ipinfo.io/{ip_address}/json")
    
    if response.status_code == 200:
        data = response.json()
        if 'loc' in data:
            # Split the 'loc' string into latitude and longitude
            latitude, longitude = data['loc'].split(',')
            return float(latitude), float(longitude)
        else:
            print("Could not retrieve location for this IP.")
            return None
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None

def parse_filename_to_bounds(filename):
    match = re.match(r"(\d+)_DEM_y(-?\d+)x(-?\d+)\.tif", filename)
    if not match:
        raise ValueError("Invalid file name format")

    size = int(match.group(1))
    lat = int(match.group(2))
    lon = int(match.group(3))
    return lat, lon, lat + size, lon + size

def is_within_bounds(lat, lon, bounds):
    min_lat, min_lon, max_lat, max_lon = bounds
    return min_lat <= lat < max_lat and min_lon <= lon < max_lon

def find_corresponding_tif(lat, lon, directory):
    for filename in os.listdir(directory):
        if filename.endswith('.tif'):
            try:
                bounds = parse_filename_to_bounds(filename)
                if is_within_bounds(lat, lon, bounds):
                    return os.path.join(directory, filename)
            except ValueError:
                continue
    return None

def save_visualization_with_coords(file_path, save_dir):
    # Extract x and y coordinates from the filename
    coords_pattern = re.compile(r"y([-]?\d+)x([-]?\d+)")
    match = coords_pattern.search(os.path.basename(file_path))
    if match:
        y_coord, x_coord = match.groups()

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
    else:
        print(f"Could not extract coordinates from filename {file_path}")

# Set the directory to save the visualized images
save_directory = "/Volumes/Extreme SSD/topg_europa/save_img"  # Replace with your actual path
if not os.path.exists(save_directory):
    os.makedirs(save_directory)

tif_directory = "/Volumes/Extreme SSD/topg_europa/tif"

# Iterate over every .tif file in the tif_directory
for filename in os.listdir(tif_directory):
    # Skip hidden/system files
    if filename.startswith('._'):
        continue

    if filename.endswith('.tif'):
        file_path = os.path.join(tif_directory, filename)
        try:
            save_visualization_with_coords(file_path, save_directory)
        except Exception as e:
            print(f"An error occurred while processing {filename}: {e}")