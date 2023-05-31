from Matrix import *


class Spline:
    
    data: (int, float) = []
    COEFF_NUM: int = 4
    
    def __init__(self, data):
        self.data = data
    
    def spline(self, nodes):
        # data = [(1, 6), (3, -2), (5, 4)]
        n = len(nodes) - 1
        equ_num = n * 4
        coefficients_number = 4
        matrix = [[0 for x in range(equ_num)] for y in range(equ_num)]
        b = [0 for x in range(equ_num)]
        # Tworzenie macierzy do interpolacji funkcjami sklejanymi
        for j in range(0, len(nodes) - 1):
            h = nodes[j+1][0] - nodes[j][0]
            # 1. S_j(x_j) = f(x_j) =>
            #    a_j + b_j(x - x_j) + c_j(x - x_j)^2 + d_j(x - x_j)^3 =
            #    = a_j + b_j(x_j - x_j) + c_j(x_j - x_j)^2 + d_j(x_j - x_j)^3 = a_j
            matrix[coefficients_number * j][coefficients_number * j] = 1
            b[4 * j] = nodes[j][1]
            # 2. S_(j)(x_{j+1}) = f(x_{j+1})
            # factor i
            for i in range(coefficients_number):
                matrix[coefficients_number * j + 1][coefficients_number * j + i] = h ** i
                b[coefficients_number * j + 1] = nodes[j + 1][1]
            # 3. S'_{j-1}(x_j) = S'_{j}(x_j) =>
            # S'_{j-1}(x_j) = b_{j-1} + 2c_{j-1}(x_j - x_{j-1} + 3d_{j-1}(x_j - x_{j-1})^2
            # S'_{j-1}(x_j) = b_{j} => S'_{j-1}(x_j) - b_{j} = 0
            if j > 0:
                for i in range(coefficients_number):
                    if i == 0:
                        matrix[coefficients_number * (j - 1) + 2][i + coefficients_number * (j - 1)] = i
                    else:
                        matrix[coefficients_number * (j - 1) + 2][i + coefficients_number * (j - 1)] = i * h ** (i - 1)
                matrix[coefficients_number * (j - 1) + 2][1 + coefficients_number * j] = -1
            # 4. S''_{j-1}(x_j) = S''_{j}(x_j) =>
            # S''_{j-1}(x_j) = 2c_{j-1} + 6d_{j-1} * (x_j - x_{j-1})
            # S''_{j-1}(x_j) = 2c_{j} => S''_{j-1}(x_j) - 2*c_{j} = 0
            if j > 0:
                matrix[coefficients_number * (j - 1) + 3][coefficients_number * (j - 1) + 2] = 2
                matrix[coefficients_number * (j - 1) + 3][coefficients_number * (j - 1) + 3] = 6 * h
                matrix[coefficients_number * (j - 1) + 3][coefficients_number * j + 2] = -2
            # 5. last 2 equations:
            # S''_{0}(x_0) = 0 and S''_{n-1}(x_n) = 0
            #  S''_{0}(x_0) = 0 => c_0 = 0
            #  S''_{n-1}(x_n) = 0 => 2 * c_(n-1) +
            if j == n-2:
                matrix[equ_num - 2][2] = 2
            if j == n-1:
                matrix[equ_num - 1][-2] = 2
                matrix[equ_num - 1][-1] = 6 * h
        coefficients = LU_factorization(matrix, b)
        return coefficients
    
    def spline_calc(self, x, coefficients, nodes):
        for i in range(len(nodes)-1):
            height = 0
            if nodes[i][0] <= x <= nodes[i+1][0]:
                for j in range(self.COEFF_NUM):
                    h = x - nodes[i][0]
                    height += coefficients[4 * i + j] * h**j
                break
        return height

    def spline_interpolation(self, step):
        nodes = self.data[::step]    # nodes used in interpolation
        result = []
        coefficients = self.spline(nodes)
        for x in range(0, nodes[-1][0] + 1):
            height = self.spline_calc(x, coefficients, nodes)
            result.append((x, height))
        return result, nodes
