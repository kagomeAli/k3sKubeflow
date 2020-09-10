import numpy as np
import matplotlib.pyplot as plt
import os
import cv2
from sklearn.model_selection import train_test_split
import tensorflow as tf
from keras.layers import Input, Dense, Flatten, Activation
from keras.models import Model
Datadir = os.getcwd() + "/Fabric"
Categories = ["defects", "overkills"]

training_data = []
size = 64

def get_file_path(root_path,file_list=[],dir_list=[]):
    #获取该目录下所有的文件名称和目录名称
    dir_or_files = os.listdir(root_path)
    for dir_file in dir_or_files:
        #获取目录或者文件的路径
        dir_file_path = os.path.join(root_path,dir_file)
        #判断该路径为文件还是路径
        if os.path.isdir(dir_file_path):
            dir_list.append(dir_file_path)
            #递归获取所有文件和目录的路径
            get_file_path(dir_file_path,file_list,dir_list)
        else:
            file_list.append(dir_file_path)
    return file_list,dir_list

for category in Categories:
    path = os.path.join(Datadir, category)
    class_num = Categories.index(category)
    file_list,dir_list = get_file_path(path)
    for file in file_list:
        if "jpg" in file:
            image = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
            image = cv2.resize(image, (size, size))
            training_data.append([image, class_num])


print(len(training_data))

X = []
Y = []

for features, label in training_data:
    X.append(features)
    Y.append(label)
X = np.array(X).reshape(-1, size, size, 1)



x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.4)

x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255

print('x_train shape:', x_train.shape)
print(x_train.shape[0], 'train samples')
print(x_test.shape[0], 'test samples')

# from __future__ import print_function, division

#
y_train = tf.keras.utils.to_categorical(y_train, 2)
y_test = tf.keras.utils.to_categorical(y_test, 2)


def DNN_sample(input_shape=(64, 64, 1)):
    start = Input(input_shape)
    Ch_shape = Flatten()(start)

    d1 = Dense(64)(Ch_shape)
    d2 = Dense(32)(d1)
    d3 = Dense(16, activation='relu')(d2)
    output = Dense(2, activation='softmax')(d3)

    return Model(start, output)

DNN = DNN_sample()

DNN.compile(loss=tf.keras.losses.categorical_crossentropy,
            optimizer=tf.keras.optimizers.Adadelta(),
            metrics=['accuracy'])

training_process = DNN.fit(x_train, y_train,
                           batch_size=64,
                           epochs=30,
                           verbose=1,
                           validation_data=(x_test, y_test))

score = DNN.evaluate(x_test, y_test, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])

print(training_process.history.keys())
print(training_process.history['accuracy'])




