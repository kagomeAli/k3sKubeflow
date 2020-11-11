import json
import kfp
import kfp.dsl as dsl
import kfp.compiler as compiler

config = {
    # 创建model python的文件路径
    "modelPath": "/home/aoi1060/Downloads/fabricModel/pyfile/createModel.py",
    # 创建model依赖的PVC
    "pvolumePath": "/home/aoi1060/Downloads",
    # 创建model依赖的Images
    "model_depend_image": "yanqin/tensorflow-opencv:v1",
    # 将文件移动到IPC端依赖的Images
    "move_depend_image": "yanqin/paramiko_move:v1",
}

@dsl.pipeline(
    name="demo",
    description="......"
)

def demo_model():
    createModel = dsl.ContainerOp(
        name="create model",
        image=config["model_depend_image"],
        command=["sh", "-c"],
        arguments=["python3 " + config["modelPath"]],
        pvolumes={config["pvolumePath"]: dsl.PipelineVolume(pvc="downloads-pvc")}
    )

    moveModel = dsl.ContainerOp(
        name="Move_Model_to_IPC",
        image=config["move_depend_image"],
        pvolumes={config["pvolumePath"]: createModel.pvolume}
    )

if __name__ == "__main__":
    compiler.Compiler().compile(demo_model, __file__ + ".yaml")