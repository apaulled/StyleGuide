from PIL import Image


def testy():
    im = Image.open("./resources/test_dress.png")
    total = (0, 0, 0)
    rgb = im.convert('RGB')
    # pixels = im.load()
    for i in range(rgb.width):
        for j in range(rgb.height):
            total = (total[0] + rgb.getpixel((i, j))[0],
                     total[1] + rgb.getpixel((i, j))[1],
                     total[2] + rgb.getpixel((i, j))[2])
    divisor = im.height * im.width
    averages = tuple(round(num / divisor) for num in total)
    # im.show()
    return averages
