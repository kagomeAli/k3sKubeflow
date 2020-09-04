my_volume = dsl.VolumeOp(
        name="create-volume",
        resource_name="asd",
        size="10Gi",
        modes=dsl.VOLUME_MODE_RWO,
    )
dsl.ResourceOp(
        name="delete-volume",
        k8s_resource=my_volume.k8s_resource,
        action="delete"
    )
