import uuid


def audio(instance, filename):
    extension = filename.split(".")[-1]
    # print("The image is", extension)
    return "{}.{}".format(uuid.uuid4(), extension)