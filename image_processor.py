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
