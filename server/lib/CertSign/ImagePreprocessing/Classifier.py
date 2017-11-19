class Classifier:
    def __init__(self, image):
        self.image = image
        self.histogram = {}
        self.peaks = []

    def __normalize(self):
        maxValue = 0
        for i in self.histogram:
            if self.histogram[i] > maxValue:
                maxValue = self.histogram[i]

        for i in self.histogram:
            self.histogram[i] /= (maxValue * 255)

    def histogram(self, bounds):
        for x in range(bounds[0], bounds[2]):
            for y in range(bounds[1], bounds[3]):
                p = self.image.getpixel((x, y))
                if p in self.histogram:
                    self.histogram[p] += 1
                else:
                    self.histogram[p] = 1

        self.__normalize()
        return self.histogram

    def peaks(self):
        if len(self.peaks) > 0:
            return self.peaks

        increasing = True
        prev = -1
        for i in self.histogram:
            curr = self.histogram[i]
            if prev != -1 and curr < prev:
                if increasing:
                    self.peaks.append(prev)
                    increasing = False

            if curr > prev:
                increasing = True

            prev = i

        return self.peaks
