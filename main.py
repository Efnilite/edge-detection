from PIL import Image


def to_image(src):
    """Returns a new Image instance to perform operations on."""
    return Image.open(src)


def to_rgba(image, shrink):
    """Returns a 2D-list of all rgba values mapped to the specified detail level."""
    width = int(image.size[0] / shrink)
    height = int(image.size[1] / shrink)

    image = image.resize((width, height))
    image.show()

    pixels = list(image.getdata())
    final = []

    for y in range(height):
        final.append(pixels[(y * width):((y + 1) * width)])

    return final


def to_square(rgba):
    return " " if rgba[0] == 0 else "■"


def to_dots(pixels):
    return list(map(lambda row: list(map(to_square, row)), pixels))


def print_grid(dots):
    final = ""
    for row in dots:
        final += "".join(row) + "\n"

    print()
    print(final)
    print()


def print_frame():
    img = to_image("resources/testing/test-image-1.png")
    dots = to_dots(to_rgba(img, 8))

    print_grid(dots)


if __name__ == '__main__':
    print_frame()
