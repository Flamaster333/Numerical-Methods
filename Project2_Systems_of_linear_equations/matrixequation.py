import copy
import math
import time
import decimal
import matplotlib.pyplot as plt


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
        self.jacobi_residuum = []
        self.jacobi_iterations = []
        self.gauss_seidel_time = []
        self.gauss_seidel_residuum = []
        self.gauss_seidel_iterations = []
        self.lu_factor_time = []
        self.lu_factor_residuum = []
        self.lu_factor_iterations = []

    def showMatrixParameters(self, a1, a2, a3):
        print("|============== MATRIX PARAMETERS ==============|")
        print(f"|      a1={a1}     a2={a2}     a3={a3}     N={self.N}   \t|\n")

    @staticmethod
    def showResults(method, norm_res, op_time, iteration):
        norm_bigger_than = "Bigger than " + str(norm_res)
        print(method)
        print(f"|-> Time: {str(op_time)} [s]  \t\t\t\t|")
        print(f"|-> Iteration: {iteration}\t\t\t\t\t\t\t\t|")
        print(f"|-> Residuum: {norm_res if (norm_res < 10e9) else norm_bigger_than}  \t\t\t|\n")

    def createVectorB(self):
        for n in range(self.N):
            self.b[n] = math.sin(n * (self.f + 1))

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
        decimal.getcontext().prec = 100
        norm_res = decimal.Decimal(0)
        for i in range(len(res_vector)):
            norm_res += decimal.Decimal(res_vector[i]) ** decimal.Decimal(2)
        return math.sqrt(norm_res)

    def calcResiduumVector(self, x):
        res_vector = self.multiplyMatrixByVector(self.A, x)
        for i in range(len(res_vector)):
            res_vector[i] -= self.b[i]
        return res_vector

    def jacobiMethod(self, to_plot):
        # initial vector
        x = [1 for _ in range(self.N)]
        x_prev = copy.deepcopy(x)
        norm_res = self.norm(self.calcResiduumVector(x))

        iteration = 0
        accuracy_threshold = 10 ** (-9)
        # start timer
        start = time.time()

        while 10e9 > norm_res > accuracy_threshold:
            self.jacobi_residuum.append(norm_res)
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
        if to_plot:
            self.jacobi_time.append(j_time)
        self.showResults(f"|**************** Jacobi Method ****************|",
                         norm_res, j_time, iteration)

    def gaussSeidelMethod(self, to_plot):
        # initial vector
        x = [1 for _ in range(len(self.A))]
        x_prev = copy.deepcopy(x)
        norm_res = self.norm(self.calcResiduumVector(x))

        iteration = 0
        accuracy_threshold = 10 ** (-9)
        # start timer
        start = time.time()

        while 10e9 > norm_res > accuracy_threshold:
            self.gauss_seidel_residuum.append(norm_res)
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
        if to_plot:
            self.gauss_seidel_time.append(gs_time)
        self.showResults(f"|************* Gauss-Seidel Method *************|",
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

    def factorizationLU(self, to_plot):
        # start timer
        start = time.time()
        L, U = self.createLU()

        # forward-substitution (Ly = b)
        y = [0 for _ in range(self.N)]
        for i in range(self.N):
            tmp = 0
            for k in range(i):
                tmp += L[i][k] * y[k]
            y[i] = (self.b[i] - tmp) / L[i][i]

        # back-substitution (Ux = y)
        x = [0 for x in range(self.N)]
        for i in reversed(range(self.N)):
            tmp = 0
            for k in range(i + 1, self.N):
                tmp = tmp + U[i][k] * x[k]
            x[i] = (y[i] - tmp) / U[i][i]
        # end timer
        end = time.time()

        norm_res = self.norm(self.calcResiduumVector(x))
        lu_time = end - start
        if to_plot:
            self.lu_factor_time.append(lu_time)
        self.lu_factor_residuum.append(norm_res)
        self.showResults(f"|************** LU  Factorization **************|",
                         norm_res, lu_time, 0)

    def resizeMatrix(self, new_size):
        self.N = new_size
        self.A = [[0 for x in range(self.N)] for y in range(self.N)]
        self.b = [0 for x in range(self.N)]
        self.createVectorB()

    def showNormPlotIterB(self):
        # residuum plot EX B
        plt.yscale("log")
        line_jacobi, = plt.plot(self.jacobi_residuum, color='g', linewidth='0.8', label='Jacobi')
        line_gs, = plt.plot(self.gauss_seidel_residuum, color='b', linewidth='0.8', label='Gauss-Seidel')
        plt.legend(handles=[line_jacobi, line_gs], loc='upper left')
        plt.title("Norm of Residuum Vector Ex B")
        plt.xlabel("Iteration")
        plt.ylabel("Norm")
        plt.axis([0, 25, 10 ** (-9), 1E3])
        plt.show()
        # clearing arrays
        self.jacobi_residuum = []
        self.gauss_seidel_residuum = []

    def showNormPlotIterC(self):
        # residuum plot EX C
        plt.yscale("log")
        line_jacobi, = plt.plot(self.jacobi_residuum, color='g', linewidth='0.8', label='Jacobi')
        line_gs, = plt.plot(self.gauss_seidel_residuum, color='b', linewidth='0.8', label='Gauss-Seidel')
        plt.legend(handles=[line_jacobi, line_gs], loc='upper left')
        plt.title("Norm of Residuum Vector Ex C")
        plt.xlabel("Iteration")
        plt.ylabel("Norm")
        plt.axis([0, 70, 0, 1E10])
        plt.show()
        # clearing arrays
        self.jacobi_residuum = []
        self.gauss_seidel_residuum = []

    def showDurationPlot(self, N):
        # duration plot
        plt.yscale("log")
        line_jacobi, = plt.plot(N, self.jacobi_time, color='g', linewidth='0.8', label='Jacobi')
        line_gs, = plt.plot(N, self.gauss_seidel_time, color='b', linewidth='0.8', label='Gauss-Seidel')
        line_lu, = plt.plot(N, self.lu_factor_time, color='r', linewidth='0.8', label='LU Factorization')
        plt.legend(handles=[line_jacobi, line_gs, line_lu], loc='upper left')
        plt.title("Duration of the algorithms")
        plt.xlabel("Matrix Size - N")
        plt.ylabel("Time [s]")
        plt.axis([0, 3000, 10 ** (-1), 1E3])
        plt.show()

