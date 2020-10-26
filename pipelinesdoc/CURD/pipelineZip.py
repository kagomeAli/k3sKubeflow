import json
import kfp
import kfp.dsl as dsl

@dsl.pipeline(
    name="demo",
    description="......"
)

def demo_model():
    upZipFile = dsl.ContainerOp(
        name="Upzip file",
        image="tensorflow/tensorflow:2.3.0",
        command=["sh", "-c"],
        arguments=["python3 /home/aoi1060/Downloads/fabricModel/pyfile/upzipFile.py"],
        pvolumes={"/home/aoi1060/Downloads": dsl.PipelineVolume(pvc="downloads-pvc"),}
    )

if __name__ == "__main__":
    import kfp.compiler as compiler
    compiler.Compiler().compile(demo_model, __file__ + ".yaml")