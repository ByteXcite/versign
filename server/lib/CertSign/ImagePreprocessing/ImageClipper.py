class ImageClipper:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def getTiles(self, image):
        tiles = {}

        x = image.size[0] - (image.size[0] % self.width)
        y = image.size[1] - (image.size[1] % self.height)

        for i in range(0, x, self.width):
            for j in range(0, y, self.height):
                tiles[(i, j)] = image.crop((i, j, i + self.width, j + self.height))

        return tiles
