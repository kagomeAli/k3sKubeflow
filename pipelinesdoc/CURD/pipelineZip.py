import json
import kfp
import kfp.dsl as dsl

config = {
    # 解压文件 依赖的image
    "depend_image": "yanqin/tensorflow-opencv:v1",
    # 解压文件路径
    "unzipPath": "/home/aoi1060/Downloads/fabricModel/pyfile/unzipFile.py",
    # 解压文件依赖的PVC
    "pvolumePath": "/home/aoi1060/Downloads",
}

@dsl.pipeline(
    name="unzip",
    description="......"
)

def demo_model():
    unZipFile = dsl.ContainerOp(
        name="Upzip file",
        image=config["depend_image"],
        command=["sh", "-c"],
        arguments=["python3 " + config["unzipPath"]],
        pvolumes={config["pvolumePath"]: dsl.PipelineVolume(pvc="downloads-pvc")}
    )

if __name__ == "__main__":
    import kfp.compiler as compiler
    compiler.Compiler().compile(demo_model, __file__ + ".yaml")