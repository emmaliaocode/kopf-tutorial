# Kopf Tutorial: EphemeralVolumeClaim Operator
This repository aims to go through the [tutorial](https://kopf.readthedocs.io/en/stable/walkthrough/problem/) from Kopf Documents to create an EphemeralVolumeClaim Operator.

The EphemeralVolumeClaim Operator manages the following things:
1. Create a PersistentVolumeClaim once an EphemeralVolumeClaim was created (`@kopf.on.create`)
2. Update the size of the PersistentVolumeClaim once the size of the EphemeralVolumeClaim was updated (`@kopf.on.update`)
3. Create/update the labels of a PersistentVolumeClaim once the labels of an EphemeralVolumeClaim was created/updated (`@kopf.on.field`)
4. Delete a PersistentVolumeClaim once an EphemeralVolumeClaim was deleted (`kopf.adopt()`)

To achieve above, one CustomResourceDefinition to registry the EphemeralVolumeClaim object, a Python file to define the operator behavior as well as the appropriate RBACs setup for the operator are included in this repository.

## Directory Structure
```
.
├── Dockerfile
├── Pipfile
├── Pipfile.lock
├── README.md
├── evc.yaml
├── manifests
│   ├── crd.yaml
│   ├── deployment.yaml
│   ├── kustomization.yaml
│   └── rbac.yaml
└── src
    ├── ephemeral.py
    ├── requirements.txt
    └── template
        └── pvc.yaml

4 directories, 12 files
```
- `Dockerfile`: the dockerfile for building the operator image
- `evc.yaml`: the example yaml to create an EphemeralVolumeClaim
- `manifests/`: the yamls for deploying the operator
- `src/`: the main component of the operator, written in Python with Kopf framework

## Usage
### Deploy EphemeralVolumeClaim Operator to a Kubernetes Cluster
```
cd kopf-tutorial
kustomize build manifests | kubectl apply -f -
```
### Create an EphemeralVolumeClaim from the example yaml
```
cd kopf-tutorial
kubectl apply -f evc.yaml
```
