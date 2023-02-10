from PIL import Image


def to_image(src_folder):
    """Returns a new Image instance to perform operations on."""
    return Image.open(src_folder)


def to_luminance(image, shrink_level=8):
    """Returns a 2D-list of all rgba values mapped to the specified detail level."""
    width = int(image.size[0] / shrink_level)
    height = int(image.size[1] / shrink_level)

    image = image.resize((width, height)).convert("L")

    pixels = list(image.getdata())
    final = []

    for y in range(height):
        final.append(pixels[(y * width):((y + 1) * width)])

    return final


grays = "#@$%&?!*~^;:'+=-_,.` "


# grays = "#W@$8%M&0GRBENHFKSAX?PQD45O3YZ62TLC7UVJI1!*~wmikltbdfheagypqsjzxnrvouc^;:'+=-_,.` "
# i just used all the keys on my keyboard lol
# i prefer the smaller version since letters are distracting but if extended palette is needed you can uncomment it


def to_char(luminance):
    """Transforms a luminance value to an ASCII character."""
    return grays[int((1 - luminance / 255) * (len(grays) - 1))]
