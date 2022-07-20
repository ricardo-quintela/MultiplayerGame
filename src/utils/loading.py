from json import loads

from inverseKinematics import Skeleton, Bone, Limb

def load_skeleton(path: str) -> Skeleton:

    try:
        with open(path, "r") as model_file:
            data = model_file.read()
    except OSError:
        print(f"ERROR: While laoding model at {path}")
        return

    model = loads(data)

    bones = list()

    for bone in model["segments"]:
        bones.append(Bone(bone["a"][0], bone["a"][1], bone["length"], bone["angle"]))

    return bones