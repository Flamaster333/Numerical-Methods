

class Lagrange:

    # distances: float = []
    # heights: float = []
    data: (int, float) = []

    def __init__(self, data):
        # self.distances = distances
        # self.heights = heights
        self.data = data

    @staticmethod
    def lagrange(x, sample):
        length = len(sample)
        result = 0
        for i in range(length):
            tmp = 1.0
            for j in range(length):
                if i != j:
                    tmp *= (x - sample[j][0]) / (sample[i][0] - sample[j][0])
            result += tmp * sample[i][1]
        return result

    def lagrange_interpolation(self, step):
        nodes = self.data[::step]
        result = []
        for x in range(nodes[-1][0] + 1):
            height = self.lagrange(x, nodes)
            result.append((x, height))
        return result, nodes
