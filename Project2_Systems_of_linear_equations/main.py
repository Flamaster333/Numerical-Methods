from matrixequation import MatrixEquation

if __name__ == '__main__':
    # EX A
    matrix = MatrixEquation(185872)
    matrix.createVectorB()
    matrix.createBandMatrix(matrix.e + 5, -1, -1)

    # EX B
    matrix.jacobiMethod(False)
    matrix.gaussSeidelMethod(False)

    # EX C
    matrix.createBandMatrix(3, -1, -1)
    matrix.jacobiMethod(False)
    matrix.gaussSeidelMethod(False)

    # EX D
    matrix.factorizationLU(False)

    # EX E
    N = [100, 500, 1000, 2000, 3000]
    for matrix_size in N:
        matrix.resizeMatrix(matrix_size)
        matrix.createBandMatrix(matrix.e + 5, -1, -1)
        matrix.jacobiMethod(True)
        matrix.gaussSeidelMethod(True)
        matrix.factorizationLU(True)

    matrix.showPlots(N)
