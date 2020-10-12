import os
import shutil
import zipfile
import json
import cv2


def unzip_file(zip_src, dst_dir):
    r = zipfile.is_zipfile(zip_src)
    if r:
        fz = zipfile.ZipFile(zip_src, 'r')
        for file in fz.namelist():
            fz.extract(file, dst_dir)
        print('upzip ok')
        #os.remove(zip_src)
    else:
        print('This is not zip')

def LabInfo(flags):
    for i in flags:
        if flags[i] == True:
            return i


def ImgIsExist(val, list):
    if (val in list):
        return True
    else:
        return False


def createLabel2Img(labelList, labDir, imageList, imgDir):
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
                    label_info = LabInfo(content['flags'])
                    # 图片转举证
                    image = cv2.imread( imgDir + img_info, cv2.IMREAD_GRAYSCALE)
                    # 存图片，label
                    img_data.append(image)
                    label_data.append(label_info)
    print(img_data)
    print(label_data)
    return [img_data, label_data]

def LabelAImg():
       # 解压路径，解压后路径
       zipPath = '/home/aoi1060/Downloads/fabricModel/data/labels/'
       # 图片列表
       imagesPath = '/home/aoi1060/Downloads/fabricModel/images/'
       # 解压文件名
       zip_file_name = 'labels-json.zip'
       # 解压
       unzip_file(zipPath + zip_file_name, zipPath)
       # 获取解压后的文件列表
       labelList = os.listdir(zipPath)
       print(labelList)
       # 获取图片的文件列表
       imageList = os.listdir(imagesPath)
       print(imageList)
       img = createLabel2Img(labelList, zipPath, imageList, imagesPath)
       print('output:')
       print(img)
if __name__ == '__main__':
    LabelAImg()

