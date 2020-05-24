# liveproject_surface_water_changes_satellite_data
Project code for assignments associated with the live manning project "Monitoring Changes in Surface Water Using Satellite Image Data"

## Deliverable for Milestone-1

1. `Milestone-1.ipynb` downloads the satellite image by running the script `download_script.py` and save it as `example.jp2`
2. `example.jp2` is read using rasterio. Each band is visualized in the notebook and saved as a GeoTiff file in the world coordinate system.
3. The Geotiff file is loaded back in and various transformations and manipulations are applied and visualized in the notebook.
4. Finally, a rectangle is cropped from the original Geotiff file and saved as a png on disk.
5. The jupyter notebook is also exported as `Milestone-1.html` which can be downloaded to view the output produced on my computer setup.
