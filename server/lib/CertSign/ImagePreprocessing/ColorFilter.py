class ColorFilter:
    def calculateIntensity(self, tile):
        sum = 0
        for x in range(0, tile.size[0]):
            for y in range(0, tile.size[1]):
                sum += tile.getpixel((x, y))[0]

        return sum / (tile.size[0] * tile.size[1])

    def filterTiles(self, tiles):
        min = -1
        max = 0
        for tile in tiles:
            intensity = self.calculateIntensity(tiles[tile])

            if min == -1 or intensity < min:
                min = intensity

            elif intensity > max:
                max = intensity

        T = (min + max) / 2
        filteredTiles = {}
        for tile in tiles:
            intensity = self.calculateIntensity(tiles[tile])

            if intensity < T:
                filteredTiles[tile] = tiles[tile]

        return filteredTiles

    def createHistogram(self, tiles):
        min = ((0, 0), -1)
        colors = {}
        for index in tiles:
            colors[index] = self.calculateIntensity(tiles[index])
            if min[1] == -1 or colors[index] < min[1]:
                min = (index, colors[index])

        return colors, min
