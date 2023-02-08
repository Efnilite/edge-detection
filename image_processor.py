from PIL import Image


def to_image(src):
    """Returns a new Image instance to perform operations on."""
    return Image.open(src)


def to_luminance(image, shrink):
    """Returns a 2D-list of all rgba values mapped to the specified detail level."""
    width = int(image.size[0] / shrink)
    height = int(image.size[1] / shrink)

    image = image.resize((width, height)).convert("L")

    pixels = list(image.getdata())
    final = []

    for y in range(height):
        final.append(pixels[(y * width):((y + 1) * width)])

    return final


grays = "#@$%&?!*~^;:'+=-_,.` "


def to_char(luminance):
    """Transforms a luminance value to an ASCII character."""
    return grays[int((1 - luminance / 255) * (len(grays) - 1))]


def print_grid(pixels):
    """Prints the final pixel grid."""
    to_chars = list(map(lambda row: list(map(to_char, row)), pixels))

    print()

    for row in to_chars:
        print("".join(row))

    print()


def print_frame(file):
    try:
        img = to_image(file)
    except FileNotFoundError:
        return None

    dots = to_luminance(img, 8)

    print_grid(dots)

    return True
