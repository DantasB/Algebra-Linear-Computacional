import Matrix_Utils
import copy

def lu_decomposition(matrix):
    if(Matrix_Utils.matrix_determinant(matrix) == 0):
        return -1;

    number_of_rows    = len(matrix)
    number_of_columns = len(matrix[0])

    if(number_of_rows != number_of_columns):
        return -1

    result = copy.deepcopy(matrix)

    for k in range(number_of_rows):
        for i in range(k+1, number_of_rows):
            result[i][k] = float(result[i][k]/result[k][k])

        for j in range(k+1, number_of_columns):
            for i in range(k+1, number_of_columns):
                result[i][j] = float(result[i][j]-result[i][k]*result[k][j])

    return result


def cholesky_decomposition(matrix):
    number_of_rows    = len(matrix)
    number_of_columns = len(matrix[0])

    if(number_of_rows != number_of_columns):
        return -1

    #Check if the matrix is simetric, if not, return -1
    if(not Matrix_Utils.positive_definite(matrix)):
        return -1

    l = [[0.0] * len(matrix) for _ in range(len(matrix))]

    for i in range(len(matrix)):
        for j in range(i + 1):

            if(i==j):
                summation = sum(l[i][k]**2 for k in range(i))
                l[i][i]   = (matrix[i][i]-summation)**0.5
                continue;

            summation = sum(l[i][k]*l[j][k] for k in range(i))
            l[i][j]   = (1.0/l[j][j])*(matrix[i][j]-summation)

    return l


def solve_by_lu_decomposition(matrix_a, matrix_b):
    matrix_lu = copy.deepcopy(matrix_a)

    matrix_lu = lu_decomposition(matrix_lu)

    if(matrix_lu == -1):
        return -1

    matrix_y = Matrix_Utils.forward_substitution_(matrix_lu, matrix_b)
    return Matrix_Utils.backward_substitution(matrix_lu, matrix_y)


def solve_by_cholesky_decomposition(matrix_a, matrix_b):
    matrix_lu = copy.deepcopy(matrix_a)
    matrix_lu = cholesky_decomposition(matrix_lu)
    if(matrix_lu == -1):
        return -1

    matrix_y = Matrix_Utils.forward_substitution(matrix_lu, matrix_b, True)
    print(matrix_y)
    return Matrix_Utils.backward_substitution(Matrix_Utils.get_transposed_matrix(matrix_lu), matrix_y)


def iterative_jacobi(matrix_a, matrix_b):
    if (not Matrix_Utils.converge(matrix_a)):
        return -1

    n = len(matrix_a)

    solution_zero = [1.0 for i in range(n)]
    next_solution = [0.0 for i in range(n)]

    tol     = 10**(-3)
    residue = tol + 1

    i           = 0
    numerator   = 0
    denominator = 0

    while (residue > tol):

        for j in range(n):
            c = 0

            for k in range(n):
                if (j!=k):
                    c += (matrix_a[j][k] * solution_zero[k])

                next_solution[j] = (matrix_b[j]-c)/matrix_a[j][j]

        for z in range(n):
            numerator   += (next_solution[z]-solution_zero[z])**2
            denominator += next_solution[z]**2

        residue       = float(numerator**0.5)/(denominator**0.5)
        solution_zero = next_solution

        i += 1

    print("x1: "              , next_solution)
    print("residue: "         , residue      )
    print("iteration_number: ", i            )


def gauss_seidel(matrix_a, matrix_b):
    if (not Matrix_Utils.converge(matrix_a)):
        return -1

    n = len(matrix_a)

    solution_zero = [1.0 for i in range(n)]
    next_solution = [0.0 for i in range(n)]

    tol     = 10**(-3)
    residue = tol + 1

    i                = 0
    numerator        = 0
    denominator      = 0
    second_summation = 0
    second_summation = 0

    while (residue > tol):

        for j in range(n):
            first_summation  = Matrix_Utils.sum_of_vector_multiplication(matrix_a[j][:j], next_solution[:j])
            second_summation = Matrix_Utils.sum_of_vector_multiplication(matrix_a[j][j+1:], solution_zero[j+1:])
            next_solution[j] = (matrix_b[j] - first_summation - second_summation)/matrix_a[j][j]

        for z in range(n):
            numerator   += (next_solution[z]-solution_zero[z])**2
            denominator += next_solution[z]**2

        residue       = float(numerator**0.5)/(denominator**0.5)
        solution_zero = next_solution

        i += 1

    print("x1: "              , next_solution)
    print("residue: "         , residue      )
    print("iteration_number: ", i            )
