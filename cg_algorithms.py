import string
import math


class MetaGraphic:  # base class of all graphic classes
    def __init__(self, algorithm: string, color, points):
        self.algorithm = algorithm
        self.points = points
        self.color = color

    def getColor(self):
        return self.color

    # each subclass must overwrite draw method
    def draw(self):
        raise Exception("this graphic type haven't defined a draw method")

    def translate(self, displacement):
        self.points = translatePoints(self.points, displacement)

    def rotate(self, center, degree):
        self.points = translatePoints(self.points, (-center[0], -center[1]))
        self.points = rotatePoints(self.points, degree)
        self.points = translatePoints(self.points, center)

    def scale(self, center, times):
        self.points = translatePoints(self.points, (-center[0], -center[1]))
        self.points = scalePoints(self.points, times)
        self.points = translatePoints(self.points, center)

    # only lines can be clipped
    def clip(self, algorithm, pointA, pointB):
        raise Exception("clipping a non-line graphic")


def swapPointsXY(points):
    """
    swap x and y of all points in a point list
    return a list after the operation
    (x, y) -> (y, x)
    """
    reversedPoints = []
    for point in points:
        reversedPoints.append((point[1], point[0]))
    return reversedPoints


def flipPointsY(points):
    """
    flip y of all points in a point list
    return a list after the operation
    (x, y) -> (x, -y)
    """
    flippedPoints = []
    for point in points:
        flippedPoints.append((point[0], -point[1]))
    return flippedPoints


def flipPointsX(points):
    """
    flip x of all points in a point list
    return a list after the operation
    (x, y) -> (-x, y)
    """
    flippedPoints = []
    for point in points:
        flippedPoints.append((-point[0], point[1]))
    return flippedPoints


def translatePoints(points, displacement):
    """
    translate all points in a point list
    return a list after the operation
    (x, y) -> (x + dx, y + dy)
    """
    translatedPoints = []
    for i in range(0, len(points)):
        translatedPoints.append((points[i][0] + displacement[0], points[i][1] + displacement[1]))
    return translatedPoints


def rotatePoints(points, degree):
    """
    rotate all points in a point list clockwise, origin point as the center
    return a list after the operation
    """
    rotatedPoints = []
    radian = degree * math.pi / 180
    for i in range(0, len(points)):
        x, y = points[i][0], points[i][1]
        rotatedPoints.append((int(x * math.cos(radian) - y * math.sin(radian)),
                              int(x * math.sin(radian) + y * math.cos(radian))))
    return rotatedPoints


def scalePoints(points, times):
    """
    scale all points in a point list clockwise, origin point as the center
    return a list after the operation
    (x, y) -> (x * times, y * times)
    """
    scaledPoints = []
    for i in range(0, len(points)):
        scaledPoints.append((int(points[i][0] * times), int(points[i][1] * times)))
    return scaledPoints


class Line(MetaGraphic):
    def __init__(self, algorithm, color, start, end):
        super().__init__(algorithm, color, [start, end])
        self.clippedAll = False

    def draw(self):
        if self.clippedAll:
            return []

        result = []
        if self.algorithm == "DDA":
            result = self.drawByDDA()
        elif self.algorithm == "Bresenham":
            result = self.drawByBresenham()
        return result

    def drawByDDA(self):
        result = []
        points = self.points
        if points[0] == points[1]:
            result.append(points[0])
            return result

        # swap x and y if needed to ensure to be sampled by x
        reverseFlag = math.fabs(self.points[0][1] - self.points[1][1]) - math.fabs(
            self.points[0][0] - self.points[1][0]) > 0
        if reverseFlag:
            points = swapPointsXY(self.points)
        # ensure generating along +x
        if points[0][0] <= points[1][0]:
            start = points[0]
            end = points[1]
        else:
            start = points[1]
            end = points[0]

        # main algorithm
        gradient = float(end[1] - start[1]) / (end[0] - start[0])
        x, y = start[0], start[1]
        while x <= end[0]:
            result.append((int(x), int(y)))
            x += 1
            y += gradient

        # swap back x and y if having swapped before
        if reverseFlag:
            result = swapPointsXY(result)

        return result

    def drawByBresenham(self):
        result = []
        points = self.points

        # swap x and y if needed to ensure to be sampled by x
        reverseFlag = math.fabs(self.points[0][1] - self.points[1][1]) - math.fabs(
            self.points[0][0] - self.points[1][0]) > 0
        if reverseFlag:
            points = swapPointsXY(points)
        # flip y if needed to ensure gradient >= 0
        yFlippedFlag = (points[0][1] - points[1][1]) * (points[0][0] - points[1][0]) < 0
        if yFlippedFlag:
            points = flipPointsY(points)

        # ensure generating along +x
        if points[0][0] <= points[1][0]:
            start = points[0]
            end = points[1]
        else:
            start = points[1]
            end = points[0]

        dx = end[0] - start[0]
        dy = end[1] - start[1]

        # two corner cases, avoid obvious deviation at start
        if dx == 0:
            for y in range(start[1], end[1]):
                result.append((start[0], y))
        elif dy == 0:
            for x in range(start[0], end[0]):
                result.append((x, start[1]))
        # main algorithm
        else:
            x, y = start[0], start[1]
            decider = 2 * dy - dx
            while x <= end[0]:
                result.append((x, y))
                x += 1
                y += 1 if decider > 0 else 0
                decider += 2 * dy - (2 * dx if decider > 0 else 0)

        # flip back y if having flipped before
        if yFlippedFlag:
            result = flipPointsY(result)
        # swap back x and y if having swapped before
        if reverseFlag:
            result = swapPointsXY(result)
        return result

    def clip(self, algorithm, pointA, pointB):
        if self.clippedAll:
            return
        if algorithm == "Cohen-Sutherland":
            self.clipByCohenSutherland(pointA, pointB)
        elif algorithm == "Liang-Barsky":
            self.clipByLiangBarsky(pointA, pointB)

    def clipByCohenSutherland(self, pointA, pointB):
        left, right = (pointA[0], pointB[0]) if pointA[0] <= pointB[0] else (pointB[0], pointA[0])
        bottom, up = (pointA[1], pointB[1]) if pointA[1] <= pointB[1] else (pointB[1], pointA[1])
        start, end = self.points[0], self.points[1]

        while True:
            codeStart = Line.setPointCodeCS(start[0], left, right) + (Line.setPointCodeCS(start[1], bottom, up) << 2)
            codeEnd = Line.setPointCodeCS(end[0], left, right) + (Line.setPointCodeCS(end[1], bottom, up) << 2)

            if codeStart & codeEnd != 0:
                # not visible
                self.clippedAll = True
                break
            elif codeStart == 0 and codeEnd == 0:
                # completely visible
                break
            else:
                if getBinaryDigit(codeStart, 0) == 1:
                    start = Line.getIntersection(start, end, left, 0)
                elif getBinaryDigit(codeEnd, 0) == 1:
                    end = Line.getIntersection(start, end, left, 0)

                elif getBinaryDigit(codeStart, 1) == 1:
                    start = Line.getIntersection(start, end, right, 0)
                elif getBinaryDigit(codeEnd, 1) == 1:
                    end = Line.getIntersection(start, end, right, 0)

                elif getBinaryDigit(codeStart, 2) == 1:
                    start = Line.getIntersection(start, end, bottom, 1)
                elif getBinaryDigit(codeEnd, 2) == 1:
                    end = Line.getIntersection(start, end, bottom, 1)

                elif getBinaryDigit(codeStart, 3) == 1:
                    start = Line.getIntersection(start, end, up, 1)
                elif getBinaryDigit(codeEnd, 3) == 1:
                    end = Line.getIntersection(start, end, up, 1)

        self.points[0], self.points[1] = start, end

    @staticmethod
    def getIntersection(start, end, loc, isY):
        """
        find the intersection of this line and "x = loc" or "y =loc".
        isY is 0 for "x = loc", otherwise "y = loc"
        return the intersection point
        """
        isX = 1 - isY
        u = float(loc - start[isY]) / (end[isY] - start[isY])
        anotherLoc = int(start[isX] + u * (end[isX] - start[isX]))
        return (anotherLoc, loc) if isY == 1 else (loc, anotherLoc)

    @staticmethod
    def setPointCodeCS(loc, lower, upper):
        if loc < lower:
            return 0b01
        elif loc <= upper:
            return 0b00
        else:
            return 0b10

    def clipByLiangBarsky(self, pointA, pointB):
        left, right = (pointA[0], pointB[0]) if pointA[0] <= pointB[0] else (pointB[0], pointA[0])
        bottom, up = (pointA[1], pointB[1]) if pointA[1] <= pointB[1] else (pointB[1], pointA[1])
        start, end = self.points[0], self.points[1]

        p = [start[0] - end[0], end[0] - start[0], start[1] - end[1], end[1] - start[1]]
        q = [start[0] - left, right - start[0], start[1] - bottom, up - start[1]]

        uIns = [0]
        uOuts = [1]
        for i in range(0, 4):
            # check parallel
            if p[i] == 0:
                if q[i] < 0:
                    # not visible
                    self.clippedAll = True
                    return
                else:
                    continue

            # p[i] != 0
            u = float(q[i] / p[i])
            if p[i] < 0:
                uIns.append(u)
            else:
                uOuts.append(u)

        uIn = max(uIns)
        uOut = min(uOuts)

        if uIn > uOut:
            # not visible
            self.clippedAll = True
            return

        clippedStart = Line.getPointByU(uIn, start, end)
        clippedEnd = Line.getPointByU(uOut, start, end)

        self.points[0], self.points[1] = clippedStart, clippedEnd

    @staticmethod
    def getPointByU(u, start, end):
        """
        according to parametric line equation:
        x = x1 + u * (x2 - x1)
        y = y1 + u * (y2 - y1)
        get the point of the line by u
        """
        return int(start[0] + u * (end[0] - start[0])), int(start[1] + u * (end[1] - start[1]))


def getBinaryDigit(num, index):
    return num >> index & 0b1


class Polygon(MetaGraphic):
    def __init__(self, algorithm, color, pointList):
        super().__init__(algorithm, color, pointList)

    def draw(self):
        lineList = []
        last = self.points[len(self.points) - 1]
        result = []

        for point in self.points:
            lineList.append(Line(self.algorithm, self.color, last, point))
            last = point

        for line in lineList:
            result += line.draw()
        return result


class Rectangle(Polygon):
    def __init__(self, algorith, color, pointA, pointB):
        super().__init__(algorith, color,
                         [pointA, (pointA[0], pointB[1]), pointB, (pointB[0], pointA[1])])


class Ellipse(MetaGraphic):
    def __init__(self, algorithm: string, color, pointA, pointB):
        super().__init__(algorithm, color, [pointA, pointB])

    def draw(self):
        result = []
        if self.algorithm == "Midpoint":
            result = self.drawByMidpoint()
        return result

    def drawByMidpoint(self):
        result = []
        ellipseCenter = (
            int((self.points[0][0] + self.points[1][0]) / 2), int((self.points[0][1] + self.points[1][1]) / 2))
        rx = math.fabs(self.points[0][0] - self.points[1][0]) / 2
        ry = math.fabs(self.points[0][1] - self.points[1][1]) / 2

        # first part
        x, y = 0, int(ry)
        decider = ry ** 2 - rx ** 2 * ry + rx ** 2 / 4
        while ry ** 2 * x < rx ** 2 * y:
            result.append((x, y))
            x += 1
            y -= 1 if decider >= 0 else 0
            decider += 2 * ry ** 2 * x + ry ** 2 - \
                       (2 * rx ** 2 * y if decider >= 0 else 0)
        # second part
        decider = ry ** 2 * (x + 0.5) ** 2 + rx ** 2 * (y - 1) ** 2 - rx ** 2 * ry ** 2
        while y >= 0:
            result.append((x, y))
            y -= 1
            x += 1 if decider <= 0 else 0
            decider += rx ** 2 - 2 * rx ** 2 * y + \
                       (2 * ry ** 2 * x if decider <= 0 else 0)

        # complete the ellipse by making mirrored copies and assembling them
        result.extend(flipPointsX(result))
        result.extend(flipPointsY(result))
        # translate the ellipse from origin to the proper location
        result = translatePoints(result, ellipseCenter)
        return result

    # don't need to rotate an ellipse
    def rotate(self, center, degree):
        raise Exception("rotating an ellipse")


def isBesidePoints(pointA, pointB):
    return math.fabs(pointA[0] - pointB[0]) <= 1 and math.fabs(pointA[1] - pointB[1]) <= 1


class Curve(MetaGraphic):
    def __init__(self, algorithm: string, color, pointList):
        super().__init__(algorithm, color, pointList)

    def draw(self):
        result = []
        if self.algorithm == "Bezier":
            result = self.drawByBezier()
        elif self.algorithm == "B-spline":
            result = self.drawByBSpline(3)
        return result

    def drawByBezier(self):
        start = self.deCasteljau(0)
        end = self.deCasteljau(1.0)
        result = self.drawCurve(0, start, 1, end, self.deCasteljau)
        result.append(start)
        result.append(end)
        return result

    """general structure of drawing a curve"""

    def drawCurve(self, ul, lastPoint, un, nextPoint, generator):
        if isBesidePoints(lastPoint, nextPoint) or math.fabs(ul - un) <= 0.0001:  # avoid recursion being too deep
            return []

        u = (ul + un) / 2
        point = generator(u)

        result = self.drawCurve(ul, lastPoint, u, point, generator)
        result.extend(self.drawCurve(u, point, un, nextPoint, generator))

        if point != lastPoint and point != nextPoint:
            result.append(point)
        return result

    def deCasteljau(self, u):
        point = Curve.deCasteljauRecursive(u, self.points)
        return int(point[0]), int(point[1])

    @staticmethod
    def deCasteljauRecursive(u, points):
        if len(points) == 1:
            return points[0]

        nextPoints = []
        for i in range(len(points) - 1):
            nextPoints.append(((1 - u) * points[i][0] + u * points[i + 1][0],
                               (1 - u) * points[i][1] + u * points[i + 1][1]))
        return Curve.deCasteljauRecursive(u, nextPoints)

    def drawByBSpline(self, k):
        if len(self.points) < 4:
            return []

        uMin = float(k)
        start = self.deBoorCox(k, uMin)
        uMax = float(len(self.points) - 0.001)
        end = self.deBoorCox(k, uMax)
        result = self.drawCurve(uMin, start, uMax, end,
                                lambda u: self.deBoorCox(k, u))
        result.append(start)
        result.append(end)
        return result

    def deBoorCox(self, k, u):
        j = int(u)
        point = self.deBoorCoxRecursive(k, j, k, u)
        return int(point[0]), int(point[1])

    def deBoorCoxRecursive(self, k, i, r, u):
        if r == 0:
            return self.points[i]
        weight = (u - i) / (k + 1 - r)
        point1 = self.deBoorCoxRecursive(k, i, r - 1, u)
        point2 = self.deBoorCoxRecursive(k, i - 1, r - 1, u)
        return (weight * point1[0] + (1 - weight) * point2[0],
                weight * point1[1] + (1 - weight) * point2[1])
