from PIL import Image
from collections import namedtuple
from statistics import variance

Grid = namedtuple('Grid', 'x y width height')
Color = namedtuple('Color', 'r g b')
threshold = 0.5  # 0-1


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

    def variance1Chnl(img, avg):
        hist =
        s = 0
        for index, count in enumerate(hist):

    def averageColor(self):
        imgR, imgG, imgB = self.img.split()
        return Color(SubImage.averageColor1Chnl(imgR), SubImage.averageColor1Chnl(imgG),
                     SubImage.averageColor1Chnl(imgB))

    # returns a scaled down value 0-1 indicating detail
    def detailLevel(self):
        imgR, imgG, imgB = self.img.split()
        avgClr = self.averageColor()
        vrnc = variance(imgR.histogram)
