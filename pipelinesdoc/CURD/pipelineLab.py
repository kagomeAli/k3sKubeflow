import json
import kfp
import kfp.dsl as dsl

@dsl.pipeline(
    name="demo",
    description="......"
)

def demo_model():
    createModel = dsl.ContainerOp(
        name="create model",
        image="tensorflow/tensorflow:2.3.0",
        command=["sh", "-c"],
        arguments=["python3 /home/aoi1060/Downloads/fabricModel/pyfile/createModel.py"],
        pvolumes={"/home/aoi1060/Downloads": dsl.PipelineVolume(pvc="downloads-pvc")}
    )

    moveModel = dsl.ContainerOp(
        name="Move_Model_to_IPC",
        image="yanqin/paramiko_move:v1",
        pvolumes={"/home/aoi1060/Downloads/fabricModel": createModel.pvolume}
    )

if __name__ == "__main__":
    import kfp.compiler as compiler
    compiler.Compiler().compile(demo_model, __file__ + ".yaml")