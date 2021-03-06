import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.layers import AveragePooling2D
from tensorflow.keras.layers import MaxPooling2D, UpSampling2D
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import Activation
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Input
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import concatenate
from tensorflow.keras.activations import relu, softmax
import os, shutil

TRAINING_DATA_SIZE = 32374
VALIDATION_DATA_SIZE = 3598

IMAGE_SIZE = (128, 128)
CLASSES = 5
BATCH_SIZE = 32
MAX_EPOCH = 10

config = {
    # train 数据库所在文件路径
    "TFRecordDataset_train": r"/home/aoi1060/Downloads/fabricModel/database/train.tfrecords",
    # train 数据库所在文件路径
    "TFRecordDataset_valid": "/home/aoi1060/Downloads/fabricModel/database/valid.tfrecords",
    # 训练结束 model 保存路径
    "model_save_dir": "/home/aoi1060/Downloads/fabricModel/models/fabric/00000123",
}

def parser(record):
    # define your tfrecord again. Remember that you saved your image as a string.
    keys_to_features = {'image': tf.io.FixedLenFeature([], tf.string),
                        "label": tf.io.FixedLenFeature([], tf.int64)}

    # Load one example
    parsed_features = tf.io.parse_single_example(record, features=keys_to_features)

    # Turn your saved image string into an array
    image = tf.io.decode_raw(parsed_features['image'], tf.uint8)
    image = tf.cast(image, tf.float16) / 255.0
    image = tf.reshape(image, [IMAGE_SIZE[0], IMAGE_SIZE[1], 1])

    label = tf.cast(parsed_features["label"], tf.int32)
    label = tf.one_hot(label, CLASSES)
    label = tf.cast(label, dtype='float32')

    return image, label


if __name__ == '__main__':
    train_dataset = tf.data.TFRecordDataset(config['TFRecordDataset_train'])
    train_dataset = train_dataset.map(parser)

    train_dataset = train_dataset.shuffle(buffer_size=10000)
    train_dataset = train_dataset.repeat()
    train_dataset = train_dataset.batch(batch_size=BATCH_SIZE)

    valid_dataset = tf.data.TFRecordDataset(config['TFRecordDataset_valid'])
    valid_dataset = valid_dataset.map(parser)

    valid_dataset = valid_dataset.shuffle(buffer_size=500)
    valid_dataset = valid_dataset.repeat()
    valid_dataset = valid_dataset.batch(batch_size=BATCH_SIZE)

    input_tensor = Input(shape=(IMAGE_SIZE[0], IMAGE_SIZE[1], 1))

    # layer 1
    x = Conv2D(8, (3, 3), padding="same")(input_tensor)
    x = Activation(relu)(x)
    # x = BatchNormalization(axis=chanDim)(x)

    x = MaxPooling2D(pool_size=(3, 3))(x)

    x = Conv2D(16, (3, 3), padding="same")(x)
    x = Activation(relu)(x)
    x = MaxPooling2D(pool_size=(3, 3))(x)

    x = Conv2D(32, (3, 3), padding="same")(x)
    x = Activation(relu)(x)
    x = MaxPooling2D(pool_size=(2, 2))(x)

    x = Conv2D(64, (3, 3), padding="same")(x)
    x = Activation(relu)(x)
    x = MaxPooling2D(pool_size=(2, 2))(x)

    x = Flatten()(x)
    x = Dropout(0.5)(x)
    x = Dense(512, activation=relu)(x)
    x = Dense(256, activation=relu, kernel_constraint=tf.keras.constraints.UnitNorm())(x)
    x = Dense(CLASSES, activation=softmax, kernel_constraint=tf.keras.constraints.UnitNorm())(x)

    model = Model(input_tensor, x)

    optimizer = tf.keras.optimizers.Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)
    model.compile(loss=tf.keras.losses.categorical_crossentropy, optimizer=optimizer, metrics=['accuracy'])

    train_history = model.fit(train_dataset,
                              epochs=MAX_EPOCH, # 10
                              steps_per_epoch=TRAINING_DATA_SIZE // BATCH_SIZE, # 32374 // 32
                              validation_data=valid_dataset,
                              validation_steps=VALIDATION_DATA_SIZE // BATCH_SIZE)

    model.save(config['model_save_dir'], save_format='tf')