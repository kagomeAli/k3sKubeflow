import os
import zipfile

def unzip_file():
    unzip_path = '/home/aoi1060/Downloads/fabricModel/labels/'
    zip_file_name = '/home/aoi1060/Downloads/labels-json.zip'
    result= {'status': '400', 'return_info': '文件不存在', 'result': False}
    r = zipfile.is_zipfile(zip_file_name)
    print('压缩包文件名')
    print(zip_file_name)
    print('压缩包是否存在')
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
        print('更新文件夹文件')
        # 解压后，删除压缩档案
        os.remove(zip_file_name)
        result= {'status': '200', 'return_info': '解压成功', 'result': False}
    else:
        print('This is not zip')
    print(result)

if __name__ == '__main__':
    unzip_file()