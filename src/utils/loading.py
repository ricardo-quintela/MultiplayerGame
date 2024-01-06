from json import loads
import logging

from inverseKinematics import Skeleton, Bone


def read_file(path: str):
    """Reads a file on the given path

    Args:
        path (str): the path to the file

    Returns:
        str: the contents of the file
    """
    # read the contents of the file
    try:
        with open(path, "r", encoding="utf-8") as model_file:
            data = model_file.read()

    except OSError:
        logging.error("While loading model at %s", path)
        return

    return data


def load_skeleton(path: str) -> Skeleton:
    """Loads the skeleton model on the given path

    Args:
        path (str): the path to the model file

    Returns:
        Skeleton: the skeleton object loaded from the json path
    """

    # read the model file
    data = read_file(path)

    # dict obtained by parsing the JSON format in the file
    model = loads(data)

    # all the bones are placed relative to the origin
    origin = model["origin"]

    # create a skeleton object
    skeleton = Skeleton()
    skeleton.set_origin(origin)

    # add the bones to the skeleton (they dont need to be in order because
    # the skeleton object allows hash searching by the name of the bone/limb)
    for bone in model["segments"]:
        skeleton.add(
            Bone(
                bone["a"][0] + origin[0],
                bone["a"][1] + origin[1],
                bone["length"],
                bone["angle"],
                bone["name"]
            )
        )


    #? create limbs with connected bones
    # iterate through all the segments
    for i in range(len(model["segments"])):

        # if the segment is linked to some other
        if model["segments"][i]["links"][0]:

            # get the segment that is linked to it
            parent = model["segments"][i]["links"][0]

            # and the name of the bone
            name = model["segments"][i]["name"]

            # create a limb object and attach them together
            skeleton.new_limb(parent)
            skeleton.get_limb(parent).add(skeleton.get_bone(parent))
            skeleton.get_limb(parent).add(skeleton.get_bone(name))


    #?anchor bones to others
    # iterate through all the segments
    for i in range(len(model["segments"])):

        # if the segment is anchored to some other
        if model["segments"][i]["links"][1]:

            # get the information about which bone and the point its anchored to
            anchor = model["segments"][i]["links"][1].split(".")

            # get the anchor bone
            bone = skeleton.get_bone(anchor[0])

            # get the point the bone is anchored to
            if anchor[1] == "a":
                point = bone.a
            else:
                point = bone.b

            # try to anchor a limb, if the limb doesnt exist, then anchor a bone
            try:
                skeleton.get_limb(model["segments"][i]["name"]).fixate(point)

            except KeyError:
                skeleton.get_bone(model["segments"][i]["name"]).fixate(point)

    return skeleton
