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
    matrix.createBandMatrix(3, -1, -1)
    matrix.jacobiMethod()
    matrix.gaussSeidelMethod()

    # for i in range(15):
        # for j in range(15):
            # print(matrix.A[i][j], end=' ')
        # print("")