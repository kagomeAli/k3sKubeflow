import numpy as np
import matplotlib.pyplot as plt
import os
import cv2
from sklearn.model_selection import train_test_split
import tensorflow as tf
from keras.layers import Input, Dense, Flatten, Activation
from keras.models import Model
Datadir = os.getcwd() + "/Fabric"
Categories = ["overkill/edges"]

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


def AE_sample(input_shape = (28, 28, 1)):
   start = Input(input_shape)

   c1_1 = Conv2D(16, (3, 3), activation='relu' ,padding='same')(start)
   c1_2 = MaxPool2D((2, 2), padding='same')(c1_1)

   c2_1 = UpSampling2D((2, 2))(c1_2)
   c2_2 = Conv2D(16, (3, 3), activation='relu' ,padding='same')(c2_1)

   output = Conv2D(1, (3, 3), activation='sigmoid' ,padding='same')(c2_2)

   return Model(start, output)

AE = AE_sample()
   # Compile model
AE.compile(loss=tf.keras.losses.MSE,
         optimizer=tf.keras.optimizers.Adadelta())

# Start training
training_process = AE.fit(x_train, x_train,
         batch_size=64,
         epochs=30,
         verbose=1,
         validation_data=(x_test, x_test))

# Rebuild Image
result = AE.predict(x_test)

n = 10
plt.figure(figsize=(20, 4))
for i in range(n):
    ax = plt.subplot(2, n, i + 1)
    plt.imshow(x_test[i].reshape(28, 28))
    plt.gray()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    ax = plt.subplot(2, n, i + 1 + n)
    plt.imshow(result[i].reshape(28, 28))
    plt.gray()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
plt.show()

