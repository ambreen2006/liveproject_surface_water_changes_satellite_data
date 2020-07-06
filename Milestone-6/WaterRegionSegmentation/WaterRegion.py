import os
import rasterio
from rasterio.plot import reshape_as_image

import tensorflow as tf

import numpy as np

from CustomModel.UNETModel import unet_residual

class WaterRegion(object):

    def __init__(self):

        self.model = unet_residual()
        self.default_width = 256
        self.default_height = 256
        self.default_channels = 3
        self.model._model.load_weights('CustomModel/model.h5')

    def inputSize(self):
        return (self.default_height, self.default_width, self.default_channels)

    def identifyRegion(self, input_images,
                       normalize_input = True,
                       normalize_output = True,
                       output_threshold = 0.5):

        if input_images.ndim == 3:
            input_images = np.expand_dims(input_images, axis=0)

        if normalize_input:
            input_images = input_images/255

        pred = self.model.predict(input_images)
        if normalize_output:
            pred[pred > output_threshold] = 1
            pred[pred != 1] = 0

        return pred

    def convertFromJP2(self, jp2_img):

        with rasterio.open(jp2_img,
            driver='JP2OpenJPEG') as dataset:
                return reshape_as_image(dataset.read())

    def defrost(self, image, threshold = 200, replacement_value = 50):

        defrosted = np.copy(image)
        for i in range(0, image.shape[1]):
            for j in range(0, image.shape[0]):
                if np.all(list(map(lambda x: x >= threshold , image[i][j]))):
                    defrosted[i][j] = [replacement_value,
                                       replacement_value,
                                       replacement_value]
        return defrosted

    def denoise(self, image, threshold, strides = (4, 4)):

        denoised_image = np.copy(image)
        for i in range(0, image.shape[0]):
            for j in range(0, image.shape[1]):
                left = j - strides[1]
                if left < 0:
                    left = 0
                right = j + strides[1]
                if right >= image.shape[1]:
                    right = image.shape[1]-1
                up = i - strides[0]
                if up < 0:
                    up = 0
                down = i + strides[1]
                if down >= image.shape[0]:
                    down = image.shape[0]-1

                val = np.mean(image[up:down, left:right])
                if val > threshold:
                    val = 1
                else:
                    val = 0
                denoised_image[i][j] = val
        return denoised_image

    def compositeMask(self, image1, image2, index1=0, index2=2):

        h = image1.shape[0]
        w = image1.shape[1]

        image1_mask = np.zeros((w, h, 3))
        image2_mask = np.zeros((w, h, 3))

        image1_mask[:,:,index1] = image1[:,:]
        image2_mask[:,:,index2] = image2[:,:]
        return (image1_mask+image2_mask)

    def iou(self, mask_true, mask_predicted):

        i = tf.reduce_sum(mask_true*mask_predicted)
        u = tf.reduce_sum(mask_true + mask_predicted) - i
        iou = (i/u)
        return iou

    def netChange(self, mask1, mask2):

        delta = tf.reduce_sum(mask1 - mask2)
        return delta
