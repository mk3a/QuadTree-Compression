from PIL import Image
from collections import namedtuple
from statistics import variance
import logging
Grid = namedtuple('Grid', 'x y width height')
Color = namedtuple('Color', 'r g b')
THRESHOLD = 0.5  # 0-100
MAX_VARIANCE = 255 ** 2
MAX_DEPTH = 10
Logger = logging.getLogger("Logger")
Logger.setLevel(logging.INFO)
class SubImage:
    def __init__(self, img, grid=None):
        if (grid is None):
            self.grid = Grid(0, 0, img.size[0], img.size[1])
        else:
            self.grid = grid
        self.img = img

    # def __init__(self, x, y, img):
    #     self.grid = Grid(x, y, img.size[0], img.size[1])
    #     self.img = img
    def getCroppedImg(self):
        return self.img.crop((self.grid.x, self.grid.y, self.grid.x + self.grid.width, self.grid.y + self.grid.height))

    def isTooSmall(self):
        return self.grid.width < 30 or self.grid.height < 30
    def averageColor1Chnl(img):
        hist = img.histogram()
        s = 0
        for index, count in enumerate(hist):
            s += (index * count)
        return int(s / sum(hist))

    def variance(img, avg):
        hist = img.histogram()
        sqrSum = 0
        for index, count in enumerate(hist):
            sqrSum += ((index - avg) ** 2) * count
        return sqrSum / sum(hist)

    def averageColor(self):
        imgR, imgG, imgB = self.getCroppedImg().split()
        return Color(SubImage.averageColor1Chnl(imgR), SubImage.averageColor1Chnl(imgG),
                     SubImage.averageColor1Chnl(imgB))

    # returns a scaled down value 0-1 indicating detail
    def detailLevel(self):
        imgR, imgG, imgB = self.getCroppedImg().split()
        avgClr = self.averageColor()
        vrnc = SubImage.variance(imgR, avgClr.r) + SubImage.variance(imgG, avgClr.g) + SubImage.variance(imgB, avgClr.b)
        return (vrnc / (MAX_VARIANCE * 3)) * 100

    def splitIntoQuads(self):
        newWidth, newHeight = (self.grid.width // 2, self.grid.height // 2)
        initialX, initialY = (self.grid.x, self.grid.y)
        Quads = []
        QuadImgs = []
        Quads.append(Grid(initialX, initialY, newWidth, newHeight))
        Quads.append(Grid(initialX + newWidth, initialY, newWidth, newHeight))
        Quads.append(Grid(initialX, initialY + newHeight, newWidth, newHeight))
        Quads.append(Grid(initialX + newWidth, initialY + newHeight, newWidth, newHeight))
        for quad in Quads:
            QuadImgs.append(SubImage(self.img, quad))
        return QuadImgs


class Node:
    depth = 0

    def __init__(self, subImg, threshold):
        self.subImg = None
        self.children = []
        self.grid = subImg.grid
        if (subImg.detailLevel() < THRESHOLD or subImg.isTooSmall()):
            renderedImg = Image.new("RGB", subImg.img.size, subImg.averageColor())
            self.subImg = SubImage(renderedImg, self.grid)
        else:
            childrenSubImgs = subImg.splitIntoQuads()
            Node.depth += 1
            for child in childrenSubImgs:
                self.children.append(Node(child, threshold))

    def isLeaf(self):
        return not self.children

    def getCorner(self):
        return (self.grid.x, self.grid.y)

    def getImg(self):
        return self.subImg.img


class QuadTree:
    def __init__(self):
        self.depth = 0
        self.root = None
        self.renderedImg = None

    def construct(self, img, threshold):
        self.root = Node(SubImage(img), threshold)
        self.renderedImg = Image.new("RGB", img.size)

    def __renderImage__(self, node):
        if (node.isLeaf()):
            self.renderedImg.paste(node.getImg(), node.getCorner())
        else:
            for child in node.children:
                self.__renderImage__(child)

    def renderImage(self):
        self.__renderImage__(self.root)

    def getRenderedImage(self):
        return self.renderedImg



def testDetailLevel():
    highDtlImg = Image.open('test.jpg')
    lowDtlImg = Image.open('test2.jpg')
    dtl1 = SubImage(highDtlImg, Grid(0, 0, highDtlImg.size[0], highDtlImg.size[1]))
    dtl2 = SubImage(lowDtlImg, Grid(0, 0, lowDtlImg.size[0], lowDtlImg.size[1]))
    print(dtl1.detailLevel(), dtl2.detailLevel())


def testNodeConstructLessThanThreshold():
    lowDtlImg = Image.open('test2.jpg')
    dtl2 = SubImage(lowDtlImg)
    Node(dtl2)


def testQuadTree():
    lowDtlImg = Image.open('test2.jpg')
    qtree = QuadTree()
    qtree.construct(lowDtlImg, THRESHOLD)
    qtree.renderImage()
    qtree.getRenderedImage().show()


testQuadTree()
