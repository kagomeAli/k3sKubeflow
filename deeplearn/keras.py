import numpy as np
import cv2
import os
import scipy.misc

data2 = np.load('./dataset/reflect/data_AE/data2/test_ae_data_32_0903.npy')
# 32 32
print(data2[0].shape)


path = "./dataset/reflect/data_AE/data2"
npy_list = os.listdir(path)
save_path = "./dataset/Img"
if not os.path.exists(save_path):
    os.mkdir(save_path)

for i in range(0, len(npy_list)):
    print(i)
    print(npy_list[i])
    npy_full_path = os.path.join(path, npy_list[i])
    img = np.load(npy_full_path) # load进来

    save_full_path = os.path.join(save_path, npy_list[i][:-4])
    scipy.misc.imsave(save_full_path, img) # 保存
# model.compile(optimizer='rmsprop', loss='categorical_crossentropy',metrics=['accuracy'])
# model.fit(train_images, train_labels, epochs=5, batch_size=64)