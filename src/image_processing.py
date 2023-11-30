from PIL import Image

from src.color_bucket import ColorBucket
from src.color_config import ColorConfig


def pick_color(pixel, config):
    if abs(pixel[0] - pixel[1]) < 10 and abs(pixel[1] - pixel[2]) < 10 and abs(pixel[2] - pixel[0]) < 10:
        return 'BROWN'

    colors = ColorBucket()

    colors.red = sum(abs(config.red[i] - pixel[i]) for i in range(0, 3))
    colors.orange = sum(abs(config.orange[i] - pixel[i]) for i in range(0, 3))
    colors.yellow = sum(abs(config.yellow[i] - pixel[i]) for i in range(0, 3))
    colors.green = sum(abs(config.green[i] - pixel[i]) for i in range(0, 3))
    colors.aqua = sum(abs(config.aqua[i] - pixel[i]) for i in range(0, 3))
    colors.blue = sum(abs(config.blue[i] - pixel[i]) for i in range(0, 3))
    colors.purple = sum(abs(config.purple[i] - pixel[i]) for i in range(0, 3))
    colors.pink = sum(abs(config.pink[i] - pixel[i]) for i in range(0, 3))
    colors.black = sum(abs(config.black[i] - pixel[i]) for i in range(0, 3))
    colors.white = sum(abs(config.white[i] - pixel[i]) for i in range(0, 3))
    colors.brown = sum(abs(config.brown[i] - pixel[i]) for i in range(0, 3))

    # print(colors)
    primary = colors.get_least()
    # print(primary)

    return primary


def key_colors(image):
    config = ColorConfig()
    colors = ColorBucket()
    rgb = image.convert('RGB')
    # pixels = im.load()
    for i in range(rgb.width):
        for j in range(rgb.height):
            pixel = rgb.getpixel((i, j))
            if not (pixel[0] > 240 and pixel[1] > 240 and pixel[2] > 240):
                # print(pixel)
                color = pick_color(pixel, config)
                colors.add_pixel(color)
    # im.show()
    print(colors)
    return colors.get_key_colors()


def average_color(image):
    total = (0, 0, 0)
    rgb = image.convert('RGB')
    # pixels = im.load()
    color_pixels = 0
    for i in range(rgb.width):
        for j in range(rgb.height):
            if rgb.getpixel((i, j)) != (255, 255, 255):
                color_pixels += 1
                total = (total[0] + rgb.getpixel((i, j))[0],
                         total[1] + rgb.getpixel((i, j))[1],
                         total[2] + rgb.getpixel((i, j))[2])
    averages = tuple(round(num / color_pixels) for num in total)
    # im.show()
    return averages

