from PIL import Image
from collections import namedtuple
from statistics import variance

Grid = namedtuple('Grid', 'x y width height')
Color = namedtuple('Color', 'r g b')
THRESHOLD = 0.5  # 0-1
MAX_VARIANCE = 255 ** 2

class SubImage:
    def __init__(self, img, grid):
        self.grid = grid
        self.img = img.crop(grid)

    def averageColor1Chnl(img):
        hist = img.histogram()
        s = 0
        for index, count in enumerate(hist):
            s += (index * count)
        return s / sum(hist)

    def variance(img, avg):
        hist = img.histogram()
        sqrSum = 0
        for index, count in enumerate(hist):
            sqrSum += ((index - avg) ** 2) * count
        return sqrSum / sum(hist)

    def averageColor(self):
        imgR, imgG, imgB = self.img.split()
        return Color(SubImage.averageColor1Chnl(imgR), SubImage.averageColor1Chnl(imgG),
                     SubImage.averageColor1Chnl(imgB))

    # returns a scaled down value 0-1 indicating detail
    def detailLevel(self):
        imgR, imgG, imgB = self.img.split()
        avgClr = self.averageColor()
        vrnc = SubImage.variance(imgR, avgClr.r) + SubImage.variance(imgG, avgClr.g) + SubImage.variance(imgB, avgClr.b)
        return vrnc / (MAX_VARIANCE * 3)


def main():
    img = Image.open('test.jpg')
    s = SubImage(img, Grid(0, 0, 1000, 1000))
    print(s.detailLevel())


main()
