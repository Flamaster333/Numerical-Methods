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
        self.A = [[0 for _ in range(self.N)] for _ in range(self.N)]
        self.b = [0 for _ in range(self.N)]
        self.jacobi_time = []
        self.jacobi_iterations = []
        self.jacobi_residual = []
        self.gauss_seidel_time = []
        self.gauss_seidel_iterations = []
        self.gauss_seidel_residual = []
        self.lu_factor_time = []
        self.lu_factor_residual = []

    def createVectorB(self):
        for n in range(self.N):
            self.b[n] = math.sin(n * (self.f + 1))

    def showMatrixParameters(self, a1, a2, a3):
        print("|============= Matrix parameters =============|")
        print(f"|-> a1={a1} a2={a2} a3={a3}")
        print(f"|-> N={self.N}\n")
        # print()

    def createBandMatrix(self, a1, a2, a3):
        self.showMatrixParameters(a1, a2, a3)
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
        new_vector = [0 for _ in range(len(matrix))]
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

    @staticmethod
    def showResults(method, norm_res, op_time, iteration):
        norm_bigger_than = "Bigger than " + str(norm_res)
        print(method)
        print(f"|-> Time: {str(op_time)} [s]")
        print(f"|-> Iteration: {iteration}")
        print(f"|-> Residuum: {norm_res if (norm_res < 10e9) else norm_bigger_than}\n")

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
        j_time = end - start
        self.jacobi_time.append(j_time)
        self.jacobi_iterations.append(iteration)
        self.showResults(f"|*************** Jacobi Method ***************|",
                         norm_res, j_time, iteration)

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
        gs_time = end - start
        self.gauss_seidel_time.append(gs_time)
        self.gauss_seidel_iterations.append(iteration)
        self.showResults(f"|************ Gauss-Seidel Method ************|",
                         norm_res, gs_time, iteration)

    def createLU(self):
        U = copy.deepcopy(self.A)
        L = [[0 for _ in range(self.N)] for _ in range(self.N)]
        # L = identity matrix
        for i in range(self.N):
            L[i][i] = 1
        # creating L i U matrix
        # algorithm from 2nd Lecture, page 25
        for k in range(self.N - 1):
            for j in range(k + 1, self.N):
                L[j][k] = U[j][k] / U[k][k]
                for m in range(k, self.N):
                    U[j][m] -= L[j][k] * U[k][m]
        return L, U

    def factorizationLU(self):
        # start timer
        start = time.time()
        L, U = self.createLU()

        # forward-substitution (Ly = b)
        y = [0 for _ in range(len(U))]
        for i in range(len(y)):
            tmp = 0
            for k in range(i):
                tmp += L[i][k] * y[k]
            y[i] = (self.b[i] - tmp) / L[i][i]

        # back-substitution (Ux = y)
        x = [0 for x in range(len(U))]
        for i in reversed(range(len(x))):
            tmp = 0
            for k in range(i + 1, len(x)):
                tmp = tmp + U[i][k] * x[k]
            x[i] = (y[i] - tmp) / U[i][i]
        # end timer
        end = time.time()

        for i in y:
            print(i, end=" ")
        print()
        for i in x:
            print(i, end=" ")
        print()
        print()

        norm_res = self.norm(self.calcResiduumVector(x))
        lu_time = end - start
        self.lu_factor_time.append(lu_time)
        self.lu_factor_residual.append(norm_res)
        self.showResults(f"|************* LU  Factorization *************|",
                         norm_res, lu_time, 0)

