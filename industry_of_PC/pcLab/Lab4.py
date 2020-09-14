import numpy as np
import tensorflow as tf
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense, Activation, Flatten, Reshape
from tensorflow.python.keras.layers import Conv2D, Conv2DTranspose, UpSampling2D
from tensorflow.keras.layers import LeakyReLU, Dropout
from tensorflow.python.keras.layers import BatchNormalization
from tensorflow.keras.optimizers import RMSprop
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import os
import cv2

Datadir = os.getcwd() + "/Fabric"
Categories = ["defects", "overkills"]

training_data = []
size = 28

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

class DCGAN(object):
    def __init__(self, img_rows=28, img_cols=28, channel=1):
        # 初始化图片的行列通道数
        self.img_rows = img_rows
        self.img_cols = img_cols
        self.channel = channel
        self.D = None  # discriminator 判别器
        self.G = None  # generator 生成器
        self.AM = None  # adversarial model 对抗模型
        self.DM = None  # discriminator model 判别模型

    # 判别模型
    def discriminator(self):
        if self.D:
            return self.D
        self.D = Sequential()
        # 定义通道数64
        depth = 64
        # dropout系数
        dropout = 0.4
        # 输入28*28*1
        input_shape = (self.img_rows, self.img_cols, self.channel)
        # 输出14*14*64
        self.D.add(Conv2D(depth * 1, 5, strides=2, input_shape=input_shape, padding='same'))
        self.D.add(LeakyReLU(alpha=0.2))
        self.D.add(Dropout(dropout))

        # 输出7*7*128
        self.D.add(Conv2D(depth * 2, 5, strides=2, padding='same'))
        self.D.add(LeakyReLU(alpha=0.2))
        self.D.add(Dropout(dropout))

        # 输出4*4*256
        self.D.add(Conv2D(depth * 4, 5, strides=2, padding='same'))
        self.D.add(LeakyReLU(alpha=0.2))
        self.D.add(Dropout(dropout))

        # 输出4*4*512
        self.D.add(Conv2D(depth * 8, 5, strides=1, padding='same'))
        self.D.add(LeakyReLU(alpha=0.2))
        self.D.add(Dropout(dropout))

        # 全连接层
        self.D.add(Flatten())
        self.D.add(Dense(1))
        self.D.add(Activation('sigmoid'))
        self.D.summary()
        return self.D

    # 生成模型
    def generator(self):
        if self.G:
            return self.G
        self.G = Sequential()
        # dropout系数
        dropout = 0.4

        # 通道数256
        depth = 64 * 4

        # 初始平面大小设置
        dim = 7
        # 全连接层，100个的随机噪声数据，7*7*256个神经网络
        self.G.add(Dense(dim * dim * depth, input_dim=100))
        self.G.add(BatchNormalization(momentum=0.9))
        self.G.add(Activation('relu'))

        # 把1维的向量变成3维数据(7,7,256)
        self.G.add(Reshape((dim, dim, depth)))
        self.G.add(Dropout(dropout))

        # 用法和 MaxPooling2D 基本相反，比如：UpSampling2D(size=(2, 2))
        # 就相当于将输入图片的长宽各拉伸一倍，整个图片被放大了
        # 上采样，采样后得到数据格式(14,14,256)
        self.G.add(UpSampling2D())

        # 转置卷积，得到数据格式(14,14,128)
        self.G.add(Conv2DTranspose(int(depth / 2), 5, padding='same'))
        self.G.add(BatchNormalization(momentum=0.9))
        self.G.add(Activation('relu'))

        # 上采样，采样后得到数据格式(28,28,128)
        self.G.add(UpSampling2D())
        # 转置卷积，得到数据格式(28,28,64)
        self.G.add(Conv2DTranspose(int(depth / 4), 5, padding='same'))
        self.G.add(BatchNormalization(momentum=0.9))
        self.G.add(Activation('relu'))

        # 转置卷积，得到数据格式(28,28,32)
        self.G.add(Conv2DTranspose(int(depth / 8), 5, padding='same'))
        self.G.add(BatchNormalization(momentum=0.9))
        self.G.add(Activation('relu'))

        # 转置卷积，得到数据格式(28,28,1)
        self.G.add(Conv2DTranspose(1, 5, padding='same'))
        self.G.add(Activation('sigmoid'))
        self.G.summary()
        return self.G

    # 定义判别模型
    def discriminator_model(self):
        if self.DM:
            return self.DM
        # 定义优化器
        optimizer = RMSprop(lr=0.0002, decay=6e-8)
        # 构建模型
        self.DM = Sequential()
        self.DM.add(self.discriminator())
        self.DM.compile(loss='binary_crossentropy', optimizer=optimizer, metrics=['accuracy'])
        return self.DM

    # 定义对抗模型
    def adversarial_model(self):
        if self.AM:
            return self.AM
        # 定义优化器
        optimizer = RMSprop(lr=0.0001, decay=3e-8)
        # 构建模型
        self.AM = Sequential()
        # 生成器
        self.AM.add(self.generator())
        # 判别器
        self.AM.add(self.discriminator())
        self.AM.compile(loss='binary_crossentropy', optimizer=optimizer, metrics=['accuracy'])
        return self.AM


class MNIST_DCGAN(object):
    def __init__(self):
        # 图片的行数
        self.img_rows = 28
        # 图片的列数
        self.img_cols = 28
        # 图片的通道数
        self.channel = 1

        for category in Categories:
            path = os.path.join(Datadir, category)
            class_num = Categories.index(category)
            file_list, dir_list = get_file_path(path)
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


        x_train, x_test, y_train, y_test  = train_test_split(X, Y, test_size=0.4)

        self.x_train = x_train / 255.0
        # 改变数据格式(samples, rows, cols, channel)
        self.x_train = self.x_train.reshape(-1, self.img_rows, self.img_cols, 1).astype(np.float32)

        # 实例化DCGAN类
        self.DCGAN = DCGAN()
        # 定义判别器模型
        self.discriminator = self.DCGAN.discriminator_model()
        # 定义对抗模型
        self.adversarial = self.DCGAN.adversarial_model()
        # 定义生成器
        self.generator = self.DCGAN.generator()

    # 训练模型
    def train(self, train_steps=2000, batch_size=256, save_interval=0):
        noise_input = None
        if save_interval > 0:
            # 生成16个100维的噪声数据
            noise_input = np.random.uniform(-1.0, 1.0, size=[16, 100])
        for i in range(train_steps):
            # 训练判别器，提升判别能力
            # 随机得到一个batch的图片数据
            images_train = self.x_train[np.random.randint(0, self.x_train.shape[0], size=batch_size), :, :, :]
            # 随机生成一个batch的噪声数据
            noise = np.random.uniform(-1.0, 1.0, size=[batch_size, 100])
            # 生成伪造的图片数据
            images_fake = self.generator.predict(noise)
            # 合并一个batch的真实图片和一个batch的伪造图片
            x = np.concatenate((images_train, images_fake))
            # 定义标签，真实数据的标签为1，伪造数据的标签为0
            y = np.ones([2 * batch_size, 1])
            y[batch_size:, :] = 0
            # 把数据放到判别器中进行判断
            d_loss = self.discriminator.train_on_batch(x, y)

            # 训练对抗模型，提升生成器的造假能力
            # 标签都定义为1
            y = np.ones([batch_size, 1])
            # 生成一个batch的噪声数据
            noise = np.random.uniform(-1.0, 1.0, size=[batch_size, 100])
            # 训练对抗模型
            a_loss = self.adversarial.train_on_batch(noise, y)
            # 打印判别器的loss和准确率，以及对抗模型的loss和准确率
            log_mesg = "%d: [D loss: %f, acc: %f]" % (i, d_loss[0], d_loss[1])
            log_mesg = "%s  [A loss: %f, acc: %f]" % (log_mesg, a_loss[0], a_loss[1])
            print(log_mesg)
            # 如果需要保存图片
            if save_interval > 0:
                # 每save_interval次保存一次
                if (i + 1) % save_interval == 0:
                    self.plot_images(save2file=True, samples=noise_input.shape[0], noise=noise_input, step=(i + 1))

    # 保存图片
    def plot_images(self, save2file=False, fake=True, samples=16, noise=None, step=0):
        filename = 'fabric.png'
        if fake:
            if noise is None:
                noise = np.random.uniform(-1.0, 1.0, size=[samples, 100])
            else:
                filename = "lab4_%d.png" % step
            # 生成伪造的图片数据
            images = self.generator.predict(noise)
        else:
            # 获得真实图片数据
            i = np.random.randint(0, self.x_train.shape[0], samples)
            images = self.x_train[i, :, :, :]

        # 设置图片大小
        plt.figure(figsize=(10, 10))
        # 生成16张图片
        for i in range(images.shape[0]):
            plt.subplot(4, 4, i + 1)
            # 获取一个张图片数据
            image = images[i, :, :, :]
            # 变成2维的图片
            image = np.reshape(image, [self.img_rows, self.img_cols])
            # 显示灰度图片
            plt.imshow(image, cmap='gray')
            # 不显示坐标轴
            plt.axis('off')
        # 保存图片
        if save2file:
            plt.savefig(filename)
            plt.close('all')
        # 不保存的话就显示图片
        else:
            plt.show()


# 实例化网络的类
fabric_dcgan = MNIST_DCGAN()
# 训练模型
fabric_dcgan.train(train_steps=2000, batch_size=256, save_interval=500)