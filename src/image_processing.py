from PIL import Image


def primary_color(image):
    total = (0, 0, 0)
    rgb = image.convert('RGB')
    # pixels = im.load()
    color_pixels = 0
    for i in range(rgb.width):
        for j in range(rgb.height):
            if rgb.getpixel((i, j)) != (0, 0, 0):
                color_pixels += 1
                total = (total[0] + rgb.getpixel((i, j))[0],
                         total[1] + rgb.getpixel((i, j))[1],
                         total[2] + rgb.getpixel((i, j))[2])
    averages = tuple(round(num / color_pixels) for num in total)
    # im.show()
    return averages

