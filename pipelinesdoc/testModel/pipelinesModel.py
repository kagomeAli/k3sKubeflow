import json
import kfp
import kfp.dsl as dsl

_CONTAINER_MANIFEST = """
{ "apiVersion": "apps/v1",
  "kind": "Deployment",
  "metadata":
  { "labels": { "app": "fabric" },
    "name": "fabric-v1",
    "namespace": "kubeflow" },
  "spec":
  { "selector": { "matchLabels": { "app": "fabric" } },
    "template":
    { "metadata":
    { "annotations": { "sidecar.istio.io/inject": "true" },
      "labels": { "app": "fabric", "version": "v1" } },
      "spec":
      { "containers":
      [ { "env":
      [ { "name": "rest_api_port", "value": "8500" },
        { "name": "port", "value": "8501" },
        { "name": "MODEL_NAME", "value": "fabric" },
        { "name": "MODEL_BASE_PATH", "value": "/mnt/1060dir/models" } ],
        "image": "tensorflow/serving:2.2.0",
        "ports": [ { "containerPort": 8501 }, { "containerPort": 8500 } ],
        "resources":
        { "limits": { "cpu": "4", "memory": "4Gi" },
          "requests": { "cpu": "1", "memory": "1Gi" } },
        "imagePullPolicy": "IfNotPresent",
        "livenessProbe":
        { "initialDelaySeconds": 30,
          "periodSeconds": 30,
          "tcpSocket": { "port": 8501 } },
        "name": "fabric",
        "volumeMounts": [ { "mountPath": "/mnt/1060dir", "name": "tf-volume" } ] } ],
        "volumes":
        [ { "name": "tf-volume",
          "hostPath": { "path": "/mnt/1060dir", "type": "Directory" } } ],
        "nodeSelector": { "name": "aoi1060" } } } } }
"""

@dsl.pipeline(
    name="VolumeOp Sequential",
    description="The third example of the design doc."
)

def volumeop_sequential():
    createModel = dsl.ContainerOp(
        name="create_model",
        image="tensorflow/tensorflow:2.3.0",
        command=["sh", "-c"],
        arguments=["python3 /data/models/dslModel.py"],
        file_outputs={'output': '/data/serving_status'},
        pvolumes={"/data": dsl.PipelineVolume(pvc="hostpath-pvc")}
    )
    with dsl.Condition(createModel.output != '1'):
        create_serving = dsl.ResourceOp(
            name='create_serving',
            k8s_resource=json.loads(_CONTAINER_MANIFEST),
            action='apply'
        )
        test_serving = dsl.ContainerOp(
            name="test_serving",
            image="yanqin/fabric:v1",
        ).after(create_serving)
    with dsl.Condition(createModel.output == '1'):
        test_serving = dsl.ContainerOp(
            name="test_serving",
            image="yanqin/fabric:v1",
        )



if __name__ == "__main__":
    import kfp.compiler as compiler
    compiler.Compiler().compile(volumeop_sequential, __file__ + ".tar.gz")