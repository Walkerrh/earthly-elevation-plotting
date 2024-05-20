import os
import numpy as np
import matplotlib.pyplot as plt
import earthpy as et
import earthpy.spatial as es
import earthpy.plot as ep
import rasterio as rio

# Turn interactive plotting off
plt.ioff()
fig = plt.figure()

# Download the data needed for this vignette
data = et.data.get_data("vignette-elevation")

# Set the home directory and get the data for the exercise
os.chdir(os.path.join(et.io.HOME, "earth-analytics"))
dtm = r"C:\Users\razer\Desktop\topg_europa\tif\10_DEM_y80x90.tif"

# Open the DEM with Rasterio
with rio.open(dtm) as src:
    elevation = src.read(1)
    # Set masked values to np.nan
    elevation[elevation < 0] = np.nan

# # Plot the data
# ep.plot_bands(
#     elevation,
#     cmap="gist_earth",
#     title="DTM Without Hillshade",
#     figsize=(10, 6),
# )


# Create and plot the hillshade with earthpy
hillshade = es.hillshade(elevation)
# hillshade_azimuth_210 = es.hillshade(elevation, azimuth=210)
# hillshade_angle_10 = es.hillshade(elevation, altitude=10)

# ep.plot_bands(
#     hillshade_azimuth_210,
#     cbar=False,
#     title="Hillshade made from DTM",
#     # figsize=(10, 6),
# )
save_directory = r"C:\Users\razer\Desktop\topg_europa\save_img_earthpy"
output_path = os.path.join(save_directory, f'yTESTxTEST.png')
ep.savefig(output_path)
plt.close()  # Close the figure to avoid displaying it


# # Plot the DEM and hillshade at the same time
# # sphinx_gallery_thumbnail_number = 5
# fig, ax = plt.subplots(figsize=(10, 6))
# ep.plot_bands(
#     elevation,
#     ax=ax,
#     cmap="terrain",
#     title="Lidar Digital Elevation Model (DEM)\n overlayed on top of a hillshade",
# )
# ax.imshow(hillshade, cmap="Greys", alpha=0.5)
# plt.show()