from ColorFilter import ColorFilter
from ImageClipper import ImageClipper


class SubjectLocator:
    def __init__(self):
        self.selected = []
        self.visited = []

    def __checkNeihbour(self, neigbour, localAverage):
        if neigbour in self.visited:
            return

        try:
            self.visited.append(neigbour)

            difference = (abs(self.colors[neigbour] - localAverage)) / float(self.colors[neigbour]) * 100
            if difference < 50:
                self.selected.append((neigbour, difference))
                self.__getSimilarNeighbours(neigbour)
        except KeyError:
            pass

    def locateSubject(self, image):
        print "Locating subject ..."

        # Divide image into 100x100 tiles
        tileX, tileY = 100, 100  # image.size[0]/10, image.size[1]/10
        print tileX, tileY
        tiles = ImageClipper(tileX, tileY).getTiles(image)

        # Filter out tiles which do not contain enough text
        filter = ColorFilter()
        tiles = filter.filterTiles(tiles)

        # Save distribution of colors in the image
        self.colors, m = filter.createHistogram(tiles)

        self.origin = m[1]
        selected = self.__getSimilarNeighbours(m[0])
        selected.append((m[0], 0))

        min = [image.size[0], image.size[1]]
        max = [0, 0]

        for point in selected:
            p = point[0]
            if p[0] < min[0]:
                min[0] = p[0]

            if p[0] > max[0]:
                max[0] = p[0]

            if p[1] < min[1]:
                min[1] = p[1]

            if p[1] > max[1]:
                max[1] = p[1]

        marginX = (max[0] - min[0]) * 0.05
        marginY = (max[1] - min[1]) * 0.05
        bounds = (min[0] - marginX, min[1] - marginY, max[0] + 2 * marginX + tileX, max[1] + 2 * marginY + tileY)
        print(bounds)
        return image.crop(bounds)

    def __getSimilarNeighbours(self, point):
        neigbours = self.__getNeighbouringPoints(point)

        for neigbour in neigbours:
            self.__checkNeihbour(neigbour, self.origin)

        return self.selected

    def __getNeighbouringPoints(self, point):
        top = (point[0], point[1] - 100)
        bottom = (point[0], point[1] + 100)
        left = (point[0] - 100, point[1])
        right = (point[0] + 100, point[1])
        return (left, right, top, bottom)
