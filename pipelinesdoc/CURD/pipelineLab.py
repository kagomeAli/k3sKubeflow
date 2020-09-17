import json
import kfp
import kfp.dsl as dsl

"""     createModel = dsl.ContainerOp(
        name="create model",
        image="tensorflow/tensorflow:2.3.0",
        command=["sh", "-c"],
        arguments=["python3 /data/pyfile/createModel.py"],
        pvolumes={"/data": dsl.PipelineVolume(pvc="fabric-pvc")}
    ) """

@dsl.pipeline(
    name="create models and move",
    description="......"
)

def volumeop_sequential():


    moveModel = dsl.ContainerOp(
        name="Move model to IPC",
        image="eeacms/rsync:latest",
        command=["sh", "-c"],
        arguments=["python /data/pyfile/scp2ipc.py"],
        pvolumes={"/data": dsl.PipelineVolume(pvc="fabric-pvc")}
    )


if __name__ == "__main__":
    import kfp.compiler as compiler
    compiler.Compiler().compile(volumeop_sequential, __file__ + ".tar.gz")