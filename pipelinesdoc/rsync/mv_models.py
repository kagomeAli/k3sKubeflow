import kfp
from kfp import dsl

def move_file():

    return dsl.ContainerOp(
        name='copy_file',
        image='stefda/rsync:latest',
        command=['/usr/bin/env', 'scp -P 21000 -r /mnt/1060dir/models/fabric nvidia@140.115.53.52:/home/nvidia/Downloads'],
    )

def mv_models():
    mv_mdls = move_file()

if __name__ == '__main__':
    kfp.compiler.Compiler().compile(mv_models, __file__ + '.yaml')