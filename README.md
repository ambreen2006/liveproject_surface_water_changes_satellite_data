# liveproject_surface_water_changes_satellite_data
Project code for assignments associated with the live manning project "Monitoring Changes in Surface Water Using Satellite Image Data"

## Deliverable for Milestone-6

The report in this milestone aims to provide an automation solution to the problem of identifying water regions in satellite images.

Satellite images from programs such as Sentinel-2 can provide time series images of specific resolutions which can then be used to analyze changes in the area of water region such as lakes over time.

The class WaterRegion is provided and examples are shown here that makes use of deep learning network trainined over satellite images to segment the region of interest.

## Deliverable for Milestone-5

Following optimization techniques were applied to the network:

  * Adaptive learning rate optimization based on monitoring the validation loss
  * Adding more layers to the network
  * Batch normalization
  * Addition of residual connections
  * Ensembling different models to make the prediction

## Deliverable for Milestone-4

Two instances of UNet models are created, one trained on NWPU images and the other on Sentinel-2 images. Both are further tested on Sentinel-2 test images.

* Data Pre-processing

  The data created in the previous milestones are further organized using the script in Scripts/data_organizer_script.py

  The hierarchy is as follows:

```
    NWPU
        \
         Test
         |    \
         |     Images
         |     |     \
         |     |      data -> *.img of actual lakes
         |     Masks
         |          \
         |           data -> mask_*.img mask images
         |
         Train
         |    \
         |     Images
         |     |     \
         |     |      data -> *.img of actual lakes
         |     Masks
         |          \
         |           data -> mask_*.img mask images
         |
    S2_Cloudless
        \
         Test
         |    \
         |     Images
         |     |     \
         |     |      data -> *.img of actual lakes
         |     Masks
         |          \
         |           data -> mask_*.img mask images
         |
         Train
         |    \
         |     Images
         |     |     \
         |     |      data -> *.img of actual lakes
         |     Masks
         |          \
         |           data -> mask_*.img mask images
         |

```

* Data Augmentation

  Data is augmented using ImageDataGenerator

* UNet Model

  Model takes 128*128 size images and output greyscale segmentation mask. The starting filter size for the model is 64

* Metrics

  binary_crossentropy is used for loss and IoU is computed as additional metric.

* Optimzation

  Adam is used with default settings.

* Training Outcome

  The val_loss improved to 0.188 and mean IoU to 0.9266

  Following result is for NWPU images from NWPU test set
![NWPU test](https://github.com/ambreen2006/liveproject_surface_water_changes_satellite_data/blob/master/Resources/nwpu_test.png)

  Following result is for S2 images test on the unet model trained on NWPU Images

  ![S2 test](https://github.com/ambreen2006/liveproject_surface_water_changes_satellite_data/blob/master/Resources/s2_test_on_nwpu_trained.png)


## Deliverable for Milestone-3

Workflow showing U-Net and FCN setup for training over dataset created in the previous milestone.

U-Net model is a fully convolutional neural network that we are using for segmentation task. This project requires binary segmentation, distinguising the water region from the rest of the spatial imagery.

The models presented here are not optimized yet as this will be covered in the next milestone.

Some of the tasks that were done at the end of the earlier milestones to show their usage are repeated and applied earlier here. Following are some of tasks performed:

1. Data Acquisition:

  Milestone-2 generated Satallite_image_Data.tar.gz which is downloaded and expanded here. It contains images and their corresponding masks along with the json file that contains the label identifier for all the images.

2. Data Pre-processing:

  * Splitting for testing: train_test_split is used on the labels list. The selected images and masks are then moved to a new hierarchy.
  * Data Generators: Four sets of ImageDataGenerator are created for testing and training on images and masks that reads the data from the specified directory.
  * The image masks are converted to greyscale using the data generator.


3. Segmentation Models:

* U-Net Model

  * The network is trained with images of size 256 * 256 with RGB channels
  * Each convolution layer uses filter size of 3 x 3.
  * Downsampling layers uses combination of convolution and max pooling.
  * Middle layer performs convolution twice on the bottleneck.
  * Then Upsampling performs deconvolution along with  concatetenating the feature information from the adjacent layer.
  * Because the padding is set to same, the cropping is not   performed.
  * Final predicted mask is greyscale
  * Early stopping callback is used along with the callback to auto-save the model in h5 format.


* FCN Model

  * A simple implementation that uses the same parameters such as image size and channels input/output specification.
  * It has similar downsampling and upsampling paths, however, features from the adjacent layers are not utilized while upsampling.


* Metrics

  * binary_crossentropy is used for loss
  * IoU is also recorded

* Image Segmentation Preview:

The images below show the mask generated by the U-Net along side the input image.

![Image Segmentation](https://github.com/ambreen2006/liveproject_surface_water_changes_satellite_data/blob/master/Milestone-3/Resources/test_segmentation.png)


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
