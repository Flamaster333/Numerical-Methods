import copy


def print_matrix(matrix):
    for i in range(len(matrix)):
        print("[", end="\t")
        for j in range(len(matrix[i])):
            print(str(matrix[i][j]), end="\t\t")
        print("]")


def print_vector(vector):
    for i in range(len(vector)):
        print("[", end="\t")
        print(vector[i], end="\t]\n")


def create_unit_matrix(N):
    unit_matrix = [[0 for x in range(N)] for y in range(N)]
    for i in range(N):
        unit_matrix[i][i] = 1
    return unit_matrix


def interchange_rows(matrix, k, index, i_from, i_to):
    matrix[k][i_from:i_to], matrix[index][i_from:i_to] = matrix[index][i_from:i_to], matrix[k][i_from:i_to]


def create_LU(matrix, N):
    U = copy.deepcopy(matrix)
    L = create_unit_matrix(N)
    P = create_unit_matrix(N)   # permutation matrix

    for k in range(N-1):
        # find pivot
        pivot = abs(U[0][k])
        index = 0
        for i in range(k, N):
            if abs(U[i][k]) > pivot:
                pivot = abs(U[i][k])
                index = i
        interchange_rows(U, k, index, k, N)
        interchange_rows(L, k, index, 0, k)
        interchange_rows(P, k, index, 0, N)

        for j in range(k+1, N):
            L[j][k] = U[j][k] / U[k][k]
            for m in range(k, N):
                U[j][m] -= L[j][k] * U[k][m]
    return U, L, P


def vector_multiply_matrix(matrix, vector):
    # can't multiply matrix with different size
    if len(matrix) != len(vector):
        return 0
    new_vector = [0 for x in range(len(matrix))]
    for i in range(len(new_vector)):
        for j in range(len(new_vector)):
            new_vector[i] += matrix[i][j] * vector[j]
    return new_vector


def LU_factorization(matrix, b):
    U, L, P = create_LU(matrix, len(matrix[0]))

    b = vector_multiply_matrix(P, b)
    # podstawienie w przód (forward-substitution)
    y = [0.0 for y in range(len(U))]
    for i in range(len(y)):
        tmp = 0
        for k in range(i):
            tmp += L[i][k] * y[k]
        y[i] = (b[i] - tmp)/L[i][i]

    # podstawienie wstecz (back-substitution)
    x = [0 for x in range(len(U))]
    for i in reversed(range(len(x))):
        tmp = 0
        for k in range(i+1, len(x)):
            tmp = tmp + U[i][k]*x[k]
        x[i] = (y[i] - tmp)/U[i][i]
    return x
