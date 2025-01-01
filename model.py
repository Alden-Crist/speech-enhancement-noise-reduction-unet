from tensorflow.keras.models import Model# type: ignore
from tensorflow.keras.layers import Input, Conv2D, LeakyReLU, MaxPooling2D, Dropout, concatenate, UpSampling2D, BatchNormalization# type: ignore
from tensorflow.keras.optimizers import Adam  # type: ignore
import tensorflow as tf
print(tf.__version__)

# Modified U-Net network with added enhancements
def unet(pretrained_weights=None, input_size=(128, 128, 1)):
    size_filter_in = 16  # Initial number of filters
    kernel_init = 'he_normal'  # Kernel initialization
    activation_layer = 'elu'  # Using ELU activation instead of LeakyReLU

    inputs = Input(input_size)

    # Contracting Path
    conv1 = Conv2D(size_filter_in, 5, activation=activation_layer, padding='same', kernel_initializer=kernel_init)(inputs)
    conv1 = BatchNormalization()(conv1)
    conv1 = LeakyReLU()(conv1)
    conv1 = Conv2D(size_filter_in, 3, activation=activation_layer, padding='same', kernel_initializer=kernel_init)(conv1)
    conv1 = BatchNormalization()(conv1)
    conv1 = LeakyReLU()(conv1)
    pool1 = MaxPooling2D(pool_size=(2, 2))(conv1)

    conv2 = Conv2D(size_filter_in*2, 5, activation=activation_layer, padding='same', kernel_initializer=kernel_init)(pool1)
    conv2 = BatchNormalization()(conv2)
    conv2 = LeakyReLU()(conv2)
    conv2 = Conv2D(size_filter_in*2, 3, activation=activation_layer, padding='same', kernel_initializer=kernel_init)(conv2)
    conv2 = BatchNormalization()(conv2)
    conv2 = LeakyReLU()(conv2)
    pool2 = MaxPooling2D(pool_size=(2, 2))(conv2)

    conv3 = Conv2D(size_filter_in*4, 5, activation=activation_layer, padding='same', kernel_initializer=kernel_init)(pool2)
    conv3 = BatchNormalization()(conv3)
    conv3 = LeakyReLU()(conv3)
    conv3 = Conv2D(size_filter_in*4, 3, activation=activation_layer, padding='same', kernel_initializer=kernel_init)(conv3)
    conv3 = BatchNormalization()(conv3)
    conv3 = LeakyReLU()(conv3)
    pool3 = MaxPooling2D(pool_size=(2, 2))(conv3)

    conv4 = Conv2D(size_filter_in*8, 5, activation=activation_layer, padding='same', kernel_initializer=kernel_init)(pool3)
    conv4 = BatchNormalization()(conv4)
    conv4 = LeakyReLU()(conv4)
    conv4 = Conv2D(size_filter_in*8, 3, activation=activation_layer, padding='same', kernel_initializer=kernel_init)(conv4)
    conv4 = BatchNormalization()(conv4)
    conv4 = LeakyReLU()(conv4)
    drop4 = Dropout(0.7)(conv4)  # Increased dropout rate
    pool4 = MaxPooling2D(pool_size=(2, 2))(drop4)

    conv5 = Conv2D(size_filter_in*16, 5, activation=activation_layer, padding='same', kernel_initializer=kernel_init)(pool4)
    conv5 = BatchNormalization()(conv5)
    conv5 = LeakyReLU()(conv5)
    conv5 = Conv2D(size_filter_in*16, 3, activation=activation_layer, padding='same', kernel_initializer=kernel_init)(conv5)
    conv5 = BatchNormalization()(conv5)
    conv5 = LeakyReLU()(conv5)
    drop5 = Dropout(0.7)(conv5)  # Increased dropout rate

    # Expanding Path
    up6 = Conv2D(size_filter_in*8, 2, activation=activation_layer, padding='same', kernel_initializer=kernel_init)(UpSampling2D(size=(2, 2))(drop5))
    up6 = LeakyReLU()(up6)
    merge6 = concatenate([drop4, up6], axis=3)
    conv6 = Conv2D(size_filter_in*8, 5, activation=activation_layer, padding='same', kernel_initializer=kernel_init)(merge6)
    conv6 = BatchNormalization()(conv6)
    conv6 = LeakyReLU()(conv6)
    conv6 = Conv2D(size_filter_in*8, 3, activation=activation_layer, padding='same', kernel_initializer=kernel_init)(conv6)
    conv6 = BatchNormalization()(conv6)
    conv6 = LeakyReLU()(conv6)

    up7 = Conv2D(size_filter_in*4, 2, activation=activation_layer, padding='same', kernel_initializer=kernel_init)(UpSampling2D(size=(2, 2))(conv6))
    up7 = LeakyReLU()(up7)
    merge7 = concatenate([conv3, up7], axis=3)
    conv7 = Conv2D(size_filter_in*4, 5, activation=activation_layer, padding='same', kernel_initializer=kernel_init)(merge7)
    conv7 = BatchNormalization()(conv7)
    conv7 = LeakyReLU()(conv7)
    conv7 = Conv2D(size_filter_in*4, 3, activation=activation_layer, padding='same', kernel_initializer=kernel_init)(conv7)
    conv7 = BatchNormalization()(conv7)
    conv7 = LeakyReLU()(conv7)

    up8 = Conv2D(size_filter_in*2, 2, activation=activation_layer, padding='same', kernel_initializer=kernel_init)(UpSampling2D(size=(2, 2))(conv7))
    up8 = LeakyReLU()(up8)
    merge8 = concatenate([conv2, up8], axis=3)
    conv8 = Conv2D(size_filter_in*2, 5, activation=activation_layer, padding='same', kernel_initializer=kernel_init)(merge8)
    conv8 = BatchNormalization()(conv8)
    conv8 = LeakyReLU()(conv8)
    conv8 = Conv2D(size_filter_in*2, 3, activation=activation_layer, padding='same', kernel_initializer=kernel_init)(conv8)
    conv8 = BatchNormalization()(conv8)
    conv8 = LeakyReLU()(conv8)

    up9 = Conv2D(size_filter_in, 2, activation=activation_layer, padding='same', kernel_initializer=kernel_init)(UpSampling2D(size=(2, 2))(conv8))
    up9 = LeakyReLU()(up9)
    merge9 = concatenate([conv1, up9], axis=3)
    conv9 = Conv2D(size_filter_in, 5, activation=activation_layer, padding='same', kernel_initializer=kernel_init)(merge9)
    conv9 = BatchNormalization()(conv9)
    conv9 = LeakyReLU()(conv9)
    conv9 = Conv2D(size_filter_in, 3, activation=activation_layer, padding='same', kernel_initializer=kernel_init)(conv9)
    conv9 = BatchNormalization()(conv9)
    conv9 = LeakyReLU()(conv9)

    # Output layer
    conv9 = Conv2D(2, 3, activation=activation_layer, padding='same', kernel_initializer=kernel_init)(conv9)
    conv9 = LeakyReLU()(conv9)
    conv10 = Conv2D(1, 1, activation='tanh')(conv9)

    # Model creation
    model = Model(inputs, conv10)

    # Compile model with Adam optimizer
    model.compile(optimizer=Adam(), loss=tf.keras.losses.Huber(), metrics=['mae'])

    # Load pretrained weights if provided
    if pretrained_weights:
        model.load_weights(pretrained_weights)

    return model
