import timeit

from PIL import Image


def to_image(src):
    return Image.open(src)


def to_rgba_getdata(image):
    sizes = image.size
    width = sizes[0]
    height = sizes[1]

    pixels = list(image.getdata())
    final = []

    for y in range(height):
        final.append(pixels[(y * width):((y + 1) * width)])

    return final


def to_rgba_getpixel(image):
    sizes = image.size
    width = sizes[0]
    height = sizes[1]

    final = []

    for y in range(height):
        row = []

        for x in range(width):
            row.append(image.getpixel((x, y)))

        final.append(row)

    return final


def to_rgba_getdata_resize(image, shrink):
    sizes = image.size
    width = sizes[0]
    height = sizes[1]

    image = image.resize((int(width / shrink), int(height / shrink)))

    pixels = list(image.getdata())
    final = []

    for y in range(height):
        final.append(pixels[(y * width):((y + 1) * width)])

    return final


n = 100
gd = timeit.timeit(lambda: to_rgba_getdata(to_image('images/test-image-2.png')), number=n)
print("=== getdata ===")
print(f"Total time: {gd} seconds")
print(f"Time per iter: {gd / n} seconds")  # 0.1 secs

gdr = timeit.timeit(lambda: to_rgba_getdata_resize(to_image('images/test-image-2.png'), 8), number=n)
print("=== getdata_resize ===")
print(f"Total time: {gdr} seconds")
print(f"Time per iter: {gdr / n} seconds")  # 0.1 secs

# gp = timeit.timeit(lambda: to_rgba_getpixel(to_image('images/test-image-2.png')), number=n)
# print("=== getpixel ===")
# print(f"Total time: {gp} seconds")
# print(f"Time per iter: {gp / n} seconds")  # 0.83 secs
