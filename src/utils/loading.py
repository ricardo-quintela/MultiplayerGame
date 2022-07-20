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

    origin = model["origin"]

    skeleton = Skeleton()

    for bone in model["segments"]:
        skeleton.add(Bone(bone["a"][0] + origin[0], bone["a"][1] + origin[1], bone["length"], bone["angle"]))

    for i in range(len(model["segments"])):
        if model["segments"][i]["links"][0]:
            index = int(model["segments"][i]["links"][0].split(".")[0])

            skeleton.newLimb(str(index))
            skeleton.getLimb(str(index)).add(skeleton.getBone(str(index)))
            skeleton.getLimb(str(index)).add(skeleton.getBone(str(i)))

    return skeleton