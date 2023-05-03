import copy
import math
import time


class MatrixEquation:

    # c - 5th digit of index number
    # d - last digit of index number
    # e - 4th digit of the index number
    # f - 3rd digit of the index number
    # N = 9cd

    def __init__(self, index_num):
        self.c = index_num % 100 // 10
        self.d = index_num % 10
        self.e = index_num % 1000 // 100
        self.f = index_num % 10_000 // 1000
        self.N = 9 * 100 + self.c * 10 + self.d
        self.A = [[0 for x in range(self.N)] for y in range(self.N)]
        self.b = [0 for x in range(self.N)]
        self.jacobi_time = []
        self.jacobi_iterations = []
        self.jacobi_residual = []
        self.gauss_seidel_time = []
        self.gauss_seidel_iterations = []
        self.gauss_seidel_residual = []

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

    @staticmethod
    def multiplyMatrixByVector(matrix, vector):
        # can't multiply matrix with different size
        if len(matrix) != len(vector):
            return 0
        new_vector = [0 for x in range(len(matrix))]
        for i in range(len(new_vector)):
            for j in range(len(new_vector)):
                new_vector[i] += matrix[i][j] * vector[j]
        return new_vector

    @staticmethod
    def norm(res_vector):
        norm_res = 0
        for i in range(len(res_vector)):
            norm_res += res_vector[i] ** 2
        return math.sqrt(norm_res)

    def calcResiduumVector(self, x):
        res_vector = self.multiplyMatrixByVector(self.A, x)
        for i in range(len(res_vector)):
            res_vector[i] -= self.b[i]
        return res_vector

    def jacobiMethod(self):
        # initial vector
        x = [1 for _ in range(len(self.A))]
        x_prev = copy.deepcopy(x)
        norm_res = self.norm(self.calcResiduumVector(x))

        iteration = 0
        accuracy_threshold = 10 ** (-9)
        # start timer
        start = time.time()

        while norm_res > accuracy_threshold:
            self.jacobi_residual.append(norm_res)
            # equation from 3rd lecture, page 13 Jacobi:
            for i in range(len(x)):
                tmp_sum = 0
                for j in range(len(x)):
                    if i != j:
                        tmp_sum += self.A[i][j] * x_prev[j]
                x[i] = (self.b[i] - tmp_sum) / self.A[i][i]
            x_prev = copy.deepcopy(x)
            iteration += 1
            norm_res = self.norm(self.calcResiduumVector(x))
        # end timer
        end = time.time()
        # printing sum up
        norm_bigger_than = "Bigger than " + str(norm_res)
        self.jacobi_time.append(end - start)
        self.jacobi_iterations.append(iteration)
        print(f"|*************** Jacobi Method ***************|")
        print(f"|-> Time: {str(end - start)} [s]")
        print(f"|-> Iteration: {iteration}")
        print(f"|-> Residuum: {norm_res if (norm_res < 10e9) else norm_bigger_than}")
        print("")

    def gaussSeidelMethod(self):
        # initial vector
        x = [1 for _ in range(len(self.A))]
        x_prev = copy.deepcopy(x)
        norm_res = self.norm(self.calcResiduumVector(x))

        iteration = 0
        accuracy_threshold = 10 ** (-9)
        # start timer
        start = time.time()

        while norm_res > accuracy_threshold:
            self.gauss_seidel_residual.append(norm_res)
            # equation from 3rd lecture, page 13 Gauss-Seidl:
            for i in range(len(x)):
                tmp_sum_1 = 0
                tmp_sum_2 = 0
                for j in range(len(x)):
                    if i > j:
                        tmp_sum_1 += self.A[i][j] * x[j]
                    elif i < j:
                        tmp_sum_2 += self.A[i][j] * x_prev[j]
                x[i] = (self.b[i] - tmp_sum_1 - tmp_sum_2) / self.A[i][i]
            x_prev = copy.deepcopy(x)
            iteration += 1
            norm_res = self.norm(self.calcResiduumVector(x))
        # end timer
        end = time.time()
        # printing sum up
        norm_bigger_than = "Bigger than " + str(norm_res)
        self.gauss_seidel_time.append(end - start)
        self.gauss_seidel_iterations.append(iteration)
        print(f"|************ Gauss-Seidel Method ************|")
        print(f"|-> Time: {str(end - start)} [s]")
        print(f"|-> Iteration: {iteration}")
        print(f"|-> Residuum: {norm_res if (norm_res < 10e9) else norm_bigger_than}")
        print("")
