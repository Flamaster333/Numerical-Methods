from matrixequation import MatrixEquation

if __name__ == '__main__':
    # EX A
    matrix = MatrixEquation(185872)
    matrix.createVectorB()
    matrix.createBandMatrix(matrix.e + 5, -1, -1)

    # EX B
    matrix.jacobiMethod()
    matrix.gaussSeidelMethod()

    # EX C
    # there are too big numbers and program crashes while doing
    # jacobi and gauss-seidel methods with a1 = 3, a2 = a3 = -1
    matrix.createBandMatrix(3, -1, -1)
    matrix.jacobiMethod()
    matrix.gaussSeidelMethod()

    # EX D
    matrix.factorizationLU()

    # EX E
    N = [100, 500, 1000, 2000, 3000]
    for matrix_size in N:
        matrix.resizeMatrix(matrix_size)
        matrix.createBandMatrix(matrix.e + 5, -1, -1)
        matrix.jacobiMethod()
        matrix.gaussSeidelMethod()
        matrix.factorizationLU()

    matrix.showPlots(N)
