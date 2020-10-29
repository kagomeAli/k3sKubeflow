import os
import shutil
import zipfile
import json
import cv2
import numpy

def LabInfo(flags, num):
    for i in flags:
        if flags[i] == True:
            return num[i]


def ImgIsExist(val, list):
    if (val in list):
        return True
    else:
        return False

def createLabel2Img(labelList, labDir, imageList, imgDir, saveDir):
    img_data = []
    label_data = []
    # createLabel2Img(labelList, zipPath, imageList, imagesPath)
    for lfile in labelList:
        if ".json" in lfile:
            img_info = lfile[:-5] + '.jpg'
            if ImgIsExist(img_info, imageList) == True:
                with open(labDir + lfile, 'r') as content_file:
                    content = content_file.read()
                    content = json.loads(content)
                    # 获取图片标签
                    label_info = LabInfo(content['flags'], content['num'])
                    # 图片转举证
                    image = cv2.imread( imgDir + img_info, cv2.IMREAD_GRAYSCALE)
                    # 存图片，label
                    img_data.append(image)
                    label_data.append(label_info)
    # 存解析后的影像文件
    print("Save the resolved image file")
    print(img_data)
    numpy.save(saveDir + "img_data.npy",img_data)
    # 存解析后的label文件
    print("Save the resolved label file")
    print(label_data)
    numpy.save(saveDir + "label_data.npy",label_data)

def unzip_file():
    unzip_path = '/home/aoi1060/Downloads/fabricModel/labels/'
    zip_file_name = '/home/aoi1060/Downloads/labels-json.zip'
    # 图片文件夹
    imagesPath = '/home/aoi1060/Downloads/fabricModel/images/'
    # 解析后的文件保存地址
    savePath = '/home/aoi1060/Downloads/fabricModel/database/'
    result= {'status': '400', 'return_info': 'file doesn\'t exist', 'result': False}
    r = zipfile.is_zipfile(zip_file_name)
    print('zip_file_name is exist')
    print(zip_file_name)
    print('Does zip_file_name exist ?')
    print(r)
    file = []
    if r:
        # 删除文件夹里的文件
        for root, dirs, files in os.walk(unzip_path):
            print(files)
            for file in files:
                os.remove(unzip_path + file)
         # 解压
        fz = zipfile.ZipFile(zip_file_name, 'r')
        for file in fz.namelist():
            fz.extract(file, unzip_path)
        print('update database')
        os.remove(zip_file_name)
        imageList = os.listdir(imagesPath)
        createLabel2Img(fz.namelist(), unzip_path, imageList, imagesPath, savePath)
        result= {'status': '200', 'return_info': 'unzip success', 'result': False}
    else:
        print('This is not zip')
    print(result)

if __name__ == '__main__':
    unzip_file()