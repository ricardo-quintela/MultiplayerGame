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
    for segment in model["segments"]:

        # if the segment is linked to some other
        if segment["links"][0]:

            # get the segment that is linked to it
            parent = segment["links"][0].split(".") if segment["links"][0] is not None else None

            # and the name of the bone
            name = segment["name"]

            # create a limb object and attach them together
            skeleton.new_limb(parent[0])
            skeleton.get_limb(parent[0]).set_master(skeleton.get_bone(parent[0]))
            skeleton.get_limb(parent[0]).set_slave(skeleton.get_bone(name), parent[1])


    #?anchor bones to others
    # iterate through all the segments
    for segment in model["segments"]:

        # if the segment is anchored to some other
        if segment["links"][1]:

            # get the information about which bone and the point its anchored to
            anchor = segment["links"][1].split(".")

            # get the anchor bone
            bone = skeleton.get_bone(anchor[0])

            # get the point the bone is anchored to
            if anchor[1] == "a":
                point = bone.a
            else:
                point = bone.b

            # try to anchor a limb, if the limb doesnt exist, then anchor a bone
            try:
                skeleton.get_limb(segment["name"]).fixate(point)

            except KeyError:
                skeleton.get_bone(segment["name"]).fixate(point, anchor[2])

    return skeleton
