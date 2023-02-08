from PIL import Image


def to_image(src):
    """Returns a new Image instance to perform operations on."""
    return Image.open(src)


def to_rgba_getdata(image, shrink):
    """Returns a 2D-list of all rgba values mapped to the specified detail level."""
    sizes = image.size
    width = sizes[0]
    height = sizes[1]

    image = image.resize((int(width / shrink), int(height / shrink)))

    pixels = list(image.getdata())
    final = []

    for y in range(height):
        print(y, pixels[(y * width):((y + 1) * width)])
        final.append(pixels[(y * width):((y + 1) * width)])

    return final


def to_square(rgba):
    return " " if rgba[0] == 0 else "■"


def to_dots(pixels):
    return list(map(lambda row: list(map(to_square, row)), pixels))


def print_grid(pixels):
    print()

    for row in pixels:
        print("".join(row))

    print()


to_rgba_getdata(to_image("images/test-image-1.png"), 8)
