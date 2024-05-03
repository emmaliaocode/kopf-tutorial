import kopf
import kubernetes
import yaml
import os


@kopf.on.create("ephemeralvolumeclaims")
def create_fn(spec, name, namespace, logger, **kwargs):

    size = spec.get("size")
    if not size:
        raise kopf.PermanentError(f"Size must be set. Got {size!r}.")

    path = os.path.join(os.path.dirname(__file__), "template/pvc.yaml")
    tmpl = open(path, "rt").read()
    text = tmpl.format(name=name, size=size)
    data = yaml.safe_load(text)

    kopf.adopt(data)  # owner references between evc & pvc

    api = kubernetes.client.CoreV1Api()
    obj = api.create_namespaced_persistent_volume_claim(
        namespace=namespace,
        body=data,
    )

    logger.info(f"PVC child is created: {obj}")

    return {"pvc-name": obj.metadata.name}


@kopf.on.update("ephemeralvolumeclaims")
def update_fn(spec, status, namespace, logger, **kwargs):

    size = spec.get("size", None)
    if not size:
        raise kopf.PermanentError(f"Size must be set. Got {size!r}.")

    pvc_name = status["create_fn"]["pvc-name"]
    pvc_patch = {"spec": {"resources": {"requests": {"storage": size}}}}

    api = kubernetes.client.CoreV1Api()
    obj = api.patch_namespaced_persistent_volume_claim(
        namespace=namespace,
        name=pvc_name,
        body=pvc_patch,
    )

    logger.info(f"PVC child is updated: {obj}")

    return {"pvc-name": obj.metadata.name}


@kopf.on.field("ephemeralvolumeclaims", field="metadata.labels")
def relabel(diff, status, namespace, logger, **kwargs):

    for op, field, old, new in diff:
        if len(field) == 0:
            labels_patch = new
        else:
            labels_patch = {field[0]: new for op, field, old, new in diff}

    pvc_name = status["create_fn"]["pvc-name"]
    pvc_patch = {"metadata": {"labels": labels_patch}}

    api = kubernetes.client.CoreV1Api()
    obj = api.patch_namespaced_persistent_volume_claim(
        namespace=namespace,
        name=pvc_name,
        body=pvc_patch,
    )

    logger.info(f"PVC child is updated: {obj}")
