import kfp.dsl as dsl

@dsl.pipeline(
    name="VolumeOp Sequential",
    description="The third example of the design doc."
)

def volumeop_sequential():
    createModel = dsl.ContainerOp(
        name="create_model",
        image="tensorflow/tensorflow:2.3.0-gpu",
        command=["sh", "-c"],
        arguments=["python3 /data/models/dslModel.py"],
        pvolumes={"/data": dsl.PipelineVolume(pvc="hostpath-pvc")}
    )



if __name__ == "__main__":
    import kfp.compiler as compiler
    compiler.Compiler().compile(volumeop_sequential, __file__ + ".tar.gz")