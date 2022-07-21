from json import loads

from inverseKinematics import Skeleton, Bone

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
        skeleton.add(Bone(bone["a"][0] + origin[0], bone["a"][1] + origin[1], bone["length"], bone["angle"], bone["name"]))

    for i in range(len(model["segments"])):
        if model["segments"][i]["links"][0]:

            parent = model["segments"][i]["links"][0]
            name = model["segments"][i]["name"]

            print(name, parent)

            skeleton.newLimb(parent)
            skeleton.getLimb(parent).add(skeleton.getBone(parent))
            skeleton.getLimb(parent).add(skeleton.getBone(name))

    for i in range(len(model["segments"])):
            
        if model["segments"][i]["links"][1]:

            anchor = model["segments"][i]["links"][1].split(".")

            bone = skeleton.getBone(anchor[0])
            if anchor[1] == "a":
                point = bone.a
            else:
                point = bone.b

            try:
                skeleton.getLimb(model["segments"][i]["name"]).fixate(point)
            except KeyError:
                skeleton.getBone(model["segments"][i]["name"]).fixate(point)


    return skeleton