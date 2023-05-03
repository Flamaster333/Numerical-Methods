import copy
import math
import time


class MatrixEquation:

    # c - 5th digit of index number
    # d - last digit of index number
    # e - 4th digit of the index number
    # f - 3rd digit of the index number
    # N = 9cd
    # index: 185872 -> N = 972

    def __init__(self, index_num):
        self.c = index_num % 100 // 10
        self.d = index_num % 10
        self.e = index_num % 1000 // 100
        self.f = index_num % 10_000 // 1000
        self.N = 9 * 100 + self.c * 10 + self.d
        self.A = [[0 for x in range(self.N)] for y in range(self.N)]
        self.b = [0 for x in range(self.N)]

    def createVectorB(self):
        for n in range(self.N):
            self.b[n] = math.sin(n * (self.f + 1))

    def createBandMatrix(self, a1, a2, a3):
        for i in range(self.N):
            for j in range(self.N):
                if i == j:
                    self.A[i][j] = a1
                elif j == i + 1 or j == i - 1:
                    self.A[i][j] = a2
                elif j == i + 2 or j == i - 2:
                    self.A[i][j] = a3
