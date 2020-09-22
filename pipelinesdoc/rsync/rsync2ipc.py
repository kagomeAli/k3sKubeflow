import os
def uploadFile2Remote():
    os.system('rsync -e "ssh -p21000" -auvz --progress --delete --bwlimit=2048 ./models/fabric/ nvidia@140.115.53.52:/home/nvidia/Downloads/fabric')

if __name__ == '__main__':
    uploadFile2Remote()