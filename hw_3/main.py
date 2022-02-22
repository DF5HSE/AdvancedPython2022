import numbers

import numpy as np


def validate_matrix_dimensions(matrix):
    if len(matrix) == 0:
        raise ValueError("Matrix is empty")
    for m in matrix:
        if len(m) != len(matrix[0]):
            raise ValueError("Rows of matrix have different sizes")


def validate_matrices_for_element_by_element_operation(m1, m2):
    if len(m1) != len(m2) or len(m1[0]) != len(m2[0]):
        raise ValueError("Matrices dimensions don't match")


def validate_matrices_for_multiply_dimensions(m1, m2):
    if len(m1[0]) != len(m2):
        raise ValueError("Matrices dimensions don't match")


class Matrix:
    check_matrix_dimensions = staticmethod(validate_matrix_dimensions)
    check_matrices_for_multiply_dimensions = staticmethod(validate_matrices_for_multiply_dimensions)
    check_matrices_for_element_by_element_operation = staticmethod(validate_matrices_for_element_by_element_operation)

    def __init__(self, matrix):
        Matrix.check_matrix_dimensions(matrix)
        self.matrix = matrix

    def __str__(self):
        return "[" + "\n".join([
            "[" + ", ".join([str(element) for element in row]) + "]"
            for row in self.matrix
        ]) + "]"

    def __element_by_element_operation(self, other, operation):
        Matrix.check_matrix_dimensions(other.matrix)
        Matrix.check_matrices_for_element_by_element_operation(self.matrix, other.matrix)
        res_matrix = []
        number_of_cols = len(self.matrix[0])
        for i in range(len(self.matrix)):
            res_matrix.append([operation(self.matrix[i][j], other.matrix[i][j]) for j in range(number_of_cols)])
        return Matrix(res_matrix)

    def __add__(self, other):
        return self.__element_by_element_operation(other, type(self.matrix[0][0]).__add__)

    def __mul__(self, other):
        return self.__element_by_element_operation(other, type(self.matrix[0][0]).__mul__)

    def __matmul__(self, other):
        Matrix.check_matrix_dimensions(other.matrix)
        Matrix.check_matrices_for_multiply_dimensions(self.matrix, other.matrix)

        res_matrix = []
        number_of_cols = len(self.matrix[0])
        for i in range(len(self.matrix)):
            row = []
            for j in range(len(self.matrix[0])):
                row.append(sum([self.matrix[i][k] * other.matrix[k][j] for k in range(number_of_cols)]))
            res_matrix.append(row)
        return Matrix(res_matrix)


class WriteMatrixMixin:
    def __init__(self, matrix):
        self.__matrix = matrix

    def write_to_file(self, path):
        with open(path, "w") as file:
            file.write(self.__str__())

    def __str__(self):
        return "[" + "\n".join([
            "[" + ", ".join([str(element) for element in row]) + "]"
            for row in self.__matrix
        ]) + "]"

    @property
    def matrix(self):
        return self.__matrix

    @matrix.setter
    def matrix(self, new_matrix):
        self.__matrix = new_matrix


class ArrayLike(np.lib.mixins.NDArrayOperatorsMixin, WriteMatrixMixin):
    def __init__(self, value):
        super().__init__(value)
        self.value = np.asarray(value)

    _HANDLED_TYPES = (np.ndarray, numbers.Number)

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        out = kwargs.get("out", ())
        for x in inputs + out:
            if not isinstance(x, self._HANDLED_TYPES + (ArrayLike,)):
                return NotImplemented

        inputs = tuple(x.value if isinstance(x, ArrayLike) else x
                       for x in inputs)
        if out:
            kwargs["out"] = tuple(
                x.value if isinstance(x, ArrayLike) else x
                for x in out)
        result = getattr(ufunc, method)(*inputs, **kwargs)

        if type(result) is tuple:
            return tuple(type(self)(x) for x in result)
        elif method == "at":
            return None
        else:
            return type(self)(result)

    def __repr__(self):
        return "%s(%r)" % (type(self).__name__, self.value)


if __name__ == "__main__":
    np.random.seed(0)
    a = Matrix(np.random.randint(0, 10, (10, 10)))
    b = Matrix(np.random.randint(0, 10, (10, 10)))
    with open("artifacts/easy/matrix+.txt", "w") as file:
        file.write((a + b).__str__())
    with open("artifacts/easy/matrix*.txt", "w") as file:
        file.write((a * b).__str__())
    with open("artifacts/easy/matrix@.txt", "w") as file:
        file.write((a @ b).__str__())

    a = ArrayLike(a.matrix)
    b = ArrayLike(b.matrix)
    (a + b).write_to_file("artifacts/medium/matrix+.txt")
    (a * b).write_to_file("artifacts/medium/matrix*.txt")
    (a @ b).write_to_file("artifacts/medium/matrix@.txt")
