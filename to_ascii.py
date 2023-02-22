from PIL import Image
import os


def to_image(src):
    """Returns a new Image instance to perform operations on."""
    return Image.open(src)


def to_luminance(image):
    """Returns a 2D-list of all rgba values mapped to the specified detail level."""
    # width = int(220)
    # height = int(63)
    terminal_size = os.get_terminal_size()
    width = int(terminal_size.columns)
    height = int(terminal_size.lines)


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


def print_grid(pixels):
    """Prints the final pixel grid with the provided pixels at the provided positions."""
    to_chars = list(map(lambda row: list(map(to_char, row)), pixels))

    total = ""

    for row in to_chars:
        total += "".join(row) + "\n"

    print(total)


def print_frame(file):
    """Prints the specified file."""
    try:
        img = to_image(file)
    except FileNotFoundError:
        return None

    dots = to_luminance(img)

    print_grid(dots)

    return True
