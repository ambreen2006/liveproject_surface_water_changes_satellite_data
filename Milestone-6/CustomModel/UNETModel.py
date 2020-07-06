import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Concatenate, Conv2DTranspose, Dropout
from tensorflow.keras.layers import BatchNormalization, Activation, Add
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, UpSampling2D

class unet_base(object):

    def __init__(self):

      self._model = None

    def train(self, train_gen, test_gen, batch, e, steps, vsteps, callbacks):

      self.history = self._model.fit(train_gen,
                                     verbose = 1,
                                     callbacks = callbacks,
                                     validation_data = test_gen,
                                     batch_size = batch,
                                     epochs = e,
                                     steps_per_epoch = steps,
                                     validation_steps = vsteps)

    def predict(self, X):

      return self._model.predict(X)

    def restore(self, pickle_path):

        self._model.load_weights(pickle_path)

class unet_residual(unet_base):

  def batchnorm_activation(self, x):

    x = BatchNormalization()(x)

    return Activation("relu")(x)

  def conv_block(self, x, filters, kernel_size=(3,3), padding='same',
                 strides=1):

    conv = self.batchnorm_activation(x)
    return Conv2D(filters, kernel_size, padding=padding, strides=strides)(conv)

  def bottleneck_block(self, x, filters, kernel_size=(3,3), padding='same',
                       strides=1):

    conv = Conv2D(filters, kernel_size, padding=padding, strides=strides)(x)
    conv = self.conv_block(conv, filters, kernel_size=kernel_size,
                           padding=padding, strides=strides)

    bottleneck = Conv2D(filters, kernel_size=(1,1), padding=padding,
                        strides=strides)(x)
    bottleneck = self.batchnorm_activation(bottleneck)
    return Add()([conv, bottleneck])

  def res_block(self, x, filters, kernel_size=(3,3), padding='same', strides=1):

    res = self.conv_block(x, filters, kernel_size=kernel_size, padding=padding,
                     strides=strides)
    res = self.conv_block(res, filters, kernel_size=kernel_size, padding=padding,
                     strides=1)
    bottleneck = Conv2D(filters, kernel_size=(1,1), padding=padding,
                        strides=strides)(x)
    bottleneck = self.batchnorm_activation(bottleneck)
    return Add()([bottleneck, res])

  def upsampling_concat_block(self, x, xskip, ff2):

    #u = UpSampling2D((2, 2))(x)
    u = Conv2DTranspose(ff2, 2, strides = (2, 2), padding = 'same')(x)
    return Concatenate()([u, xskip])

  def __init__(self, input_size = (256, 256, 3), filter = 16,
               ff2 = 128, drop_rate = 0.10):

    super(unet_residual, self).__init__()
    inputs = Input(input_size)
    layers = []

    # downsample
    e = self.bottleneck_block(inputs, filter)
    layers.append(e)

    for i in range(0, 3):
      filter = filter*2
      e = self.res_block(e, filter, strides=2)
      layers.append(e)

    _ = self.res_block(e, filter, strides=2)

    # bottleneck
    b0 = self.conv_block(_, filter, strides=1)
    u = self.conv_block(b0, filter, strides=1)

    # upsample
    for i in range(3, -1, -1):
      ff2 = ff2/2
      filter = filter/2
      u = self.upsampling_concat_block(u, layers[i], ff2)
      u = self.res_block(u, filter)

    # classify
    outputs = Conv2D(1, (1,1), padding = 'same', activation='sigmoid')(u)

    self._model = Model(inputs, outputs)
    self._model.compile(optimizer='adam',
                        loss='binary_crossentropy')
