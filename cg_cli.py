import os.path
import string
import sys

import numpy as np
import cg_algorithms as alg

from PIL import Image


class CommandParser:
    def __init__(self, outputDir):
        self.canvas = Canvas(0, 0, outputDir)

    def interpret(self, command):
        """ analyze command string """
        words = command.strip().split(' ')
        commandType = words[0]

        # comment, the line will be ignored
        if commandType == "#":
            return
        elif commandType == "resetCanvas":
            width = int(words[1])
            height = int(words[2])
            self.canvas.resetCanvas(width, height)
        elif commandType == "saveCanvas":
            name = words[1]
            self.canvas.saveCanvas(name)
        elif commandType == "setColor":
            color = (int(words[1]), int(words[2]), int(words[3]))
            self.canvas.setColor(color)
        elif commandType == "drawLine":
            gid = int(words[1])
            start = (int(words[2]), int(words[3]))
            end = (int(words[4]), int(words[5]))
            algorithm = words[6]
            self.canvas.addLine(algorithm, gid, [start, end])
        elif commandType == "drawPolygon":
            gid = int(words[1])
            pointList, end = getPointList(words, 2)
            algorithm = words[end]
            self.canvas.addPolygon(algorithm, gid, pointList)
        elif commandType == "drawRectangle":
            gid = int(words[1])
            pointA = (int(words[2]), int(words[3]))
            pointB = (int(words[4]), int(words[5]))
            algorithm = words[6]
            self.canvas.addRectangle(algorithm, gid, [pointA, pointB])
        elif commandType == "drawEllipse":
            gid = int(words[1])
            pointA = (int(words[2]), int(words[3]))
            pointB = (int(words[4]), int(words[5]))
            algorithm = "Midpoint"
            self.canvas.addEllipse(algorithm, gid, [pointA, pointB])
        elif commandType == "drawCurve":
            gid = int(words[1])
            pointList, end = getPointList(words, 2)
            algorithm = words[end]
            self.canvas.addCurve(algorithm, gid, pointList)
        elif commandType == "translate":
            gid = int(words[1])
            displacement = (int(words[2]), int(words[3]))
            self.canvas.translate(gid, displacement)
        elif commandType == "rotate":
            gid = int(words[1])
            center = (int(words[2]), int(words[3]))
            angle = int(words[4])
            self.canvas.rotate(gid, center, angle)
        elif commandType == "scale":
            gid = int(words[1])
            center = (int(words[2]), int(words[3]))
            times = float(words[4])
            self.canvas.scale(gid, center, times)
        elif commandType == "clip":
            gid = int(words[1])
            pointA = (int(words[2]), int(words[3]))
            pointB = (int(words[4]), int(words[5]))
            algorithm = words[6]
            self.canvas.clip(algorithm, gid, [pointA, pointB])


# get a pointList from command words, return pointList and the index after ones representing points
def getPointList(words, start):
    pointList = []
    i = start
    try:
        while True:
            pointList.append((int(words[i]), int(words[i + 1])))
            i += 2
    except ValueError:
        pass

    return pointList, i


class Canvas:
    def __init__(self, width, height, outputDir):
        self.tempGraphic = None
        self.width = width
        self.height = height
        self.outputDir = outputDir
        self.bitmap = np.zeros((self.height, self.width, 3), np.uint8)
        self.graphics = {}
        self.penColor = (0, 0, 0)

    def update(self):
        """ clear and then redraw all graphics """
        self.bitmap = np.zeros((self.height, self.width, 3), np.uint8)
        for gid in sorted(self.graphics.keys()):
            self.drawGraphic(self.graphics[gid])
        if self.tempGraphic is not None:
            # temporary graphic will only be drawn once
            self.drawGraphic(self.tempGraphic)
            self.tempGraphic = None

    def drawGraphic(self, graphic):
        """ draw a single graphic on bitmap """
        color = graphic.getColor()
        for x, y in graphic.draw():
            if 0 <= x < self.width and 0 <= y < self.height:
                # print(x, y)
                self.bitmap[y][x] = color

    def addGraphic(self, graphic, gid):
        if gid == -1:
            self.tempGraphic = graphic
        else:
            self.graphics[gid] = graphic

    def resetCanvas(self, width, height):
        self.height = height
        self.width = width
        self.bitmap = np.zeros((self.height, self.width, 3), np.uint8)
        self.graphics = {}

    def saveCanvas(self, name: string):
        self.update()
        Image.fromarray(self.bitmap).save(os.path.join(self.outputDir, name + ".bmp"), "BMP")

    def getImage(self):
        self.update()
        return Image.fromarray(self.bitmap)

    def setColor(self, color):
        self.penColor = color

    def addLine(self, algorithm, gid, pointList):
        if len(pointList) < 2:
            return False
        line = alg.Line(algorithm, self.penColor, pointList[0], pointList[1])
        self.addGraphic(line, gid)
        return True

    def addPolygon(self, algorithm, gid, pointList):
        polygon = alg.Polygon(algorithm, self.penColor, pointList)
        self.addGraphic(polygon, gid)
        return True

    def addRectangle(self, algorithm, gid, pointList):
        if len(pointList) < 2:
            return False
        rectangle = alg.Rectangle(algorithm, self.penColor, pointList[0], pointList[1])
        self.addGraphic(rectangle, gid)
        return True

    def addEllipse(self, algorithm, gid, pointList):
        if len(pointList) < 2:
            return False
        ellipse = alg.Ellipse(algorithm, self.penColor, pointList[0], pointList[1])
        self.addGraphic(ellipse, gid)
        return True

    def addCurve(self, algorithm, gid, pointList):
        if len(pointList) < 2:
            return False
        curve = alg.Curve(algorithm, self.penColor, pointList)
        self.addGraphic(curve, gid)
        return True

    def translate(self, gid, displacement):
        self.graphics[gid].translate(displacement)

    def rotate(self, gid, center, angle):
        self.graphics[gid].rotate(center, angle)

    def scale(self, gid, center, times):
        self.graphics[gid].scale(center, times)

    def clip(self, algorithm, gid, pointList):
        self.graphics[gid].clip(algorithm, pointList[0], pointList[1])


if __name__ == '__main__':
    argInputFile = sys.argv[1]
    argOutputDir = sys.argv[2]
    os.makedirs(argOutputDir, exist_ok=True)
    parser = CommandParser(argOutputDir)

    with open(argInputFile, 'r') as fp:
        inputLine = fp.readline()
        while inputLine:
            parser.interpret(inputLine)
            inputLine = fp.readline()
