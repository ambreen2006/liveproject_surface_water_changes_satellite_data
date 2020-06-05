# liveproject_surface_water_changes_satellite_data
Project code for assignments associated with the live manning project "Monitoring Changes in Surface Water Using Satellite Image Data"

## Deliverable for Milestone-2

Creates training and testing data set for identifying water region in satellite images. For the purpose of this milestone `NWPU-RESISC45` dataset and the dataset provided by the course is combined. Masked image label is created for each image in the combined dataset.

1. Polygons for the water region of each image is read.
2. Image mask is created from the water region and saved to disk.
3. Training and testing split is created using scikit's `train_test_split`.
4. Training set is augmented with real time transformation to help avoid over-fitting.
5. The input images and masks are then organized into a hierarchy to be used in next milestone and archived as `Satellite_Image_Data.tar.gz`

## Deliverable for Milestone-1

1. `Milestone-1.ipynb` downloads the satellite image by running the script `download_script.py` and save it as `example.jp2`
2. `example.jp2` is read using rasterio. Each band is visualized in the notebook and saved as a GeoTiff file in the world coordinate system.
3. The Geotiff file is loaded back in and various transformations and manipulations are applied and visualized in the notebook.
4. Finally, a rectangle is cropped from the original Geotiff file and saved as a png on disk.
5. The jupyter notebook is also exported as `Milestone-1.html` which can be downloaded to view the output produced on my computer setup.
