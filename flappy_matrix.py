# Imports
import random

# Network Sums
class Matrix:

    # Constructor
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.data = []

        # Initializing Matrix
        for i in range(self.rows):
            self.data.append([])
            for j in range(self.cols):
                self.data[i].append(0)

    # Copying Matrix
    def copy(self):
        m = Matrix(self.rows, self.cols)
        for i in range(self.rows):
            for j in range(self.cols):
                m.data[i][j] = self.data[i][j]
        return m

    # Creating Matrix from Array
    def fromArray(self, arr):
        m = Matrix(len(arr), 1)
        for i in range(len(arr)):
            m.data[i][0] = arr[i]
        return m

    # Creating Array from Matrix
    def toArray(self):
        arr = []
        for i in range(self.rows):
            for j in range(self.cols):
                arr.append(self.data[i][j])
        return arr

    # Randomizing Matrix
    def randomize(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.data[i][j] = (random.random() * 2) - 1

    # Adding to Matrix
    def add(self, n):
        if isinstance(n, Matrix):
            for i in range(self.rows):
                for j in range(self.cols):
                    self.data[i][j] += n.data[i][j]
        else:
            for i in range(self.rows):
                for j in range(self.cols):
                    self.data[i][j] += n
    
    # Getting New Matrix (a - b)
    def static_subtract(self, a, b):
        result = Matrix(a.rows, a.cols)
        for i in range(result.rows):
            for j in range(result.cols):
                result.data[i][j] = a.data[i][j] - b.data[i][j]
        return result

    # Reversing Matrix Dimensions
    def static_transpose(self, matrix):
        result = Matrix(matrix.cols, matrix.rows)
        for i in range(matrix.rows):
            for j in range(matrix.cols):
                result.data[j][i] = matrix.data[i][j]
        return result

    # Multiplying Value to Matrix
    def multiply(self, n):
        if isinstance(n, Matrix):  # Hadamard Product
            for i in range(self.rows):
                for j in range(self.cols):
                    self.data[i][j] *= n.data[i][j]
        else:  # Scalar Product
            for i in range(self.rows):
                for j in range(self.cols):
                    self.data[i][j] *= n

    # Apply function to all elts of Matrix
    def map(self, function):
        for i in range(self.rows):
            for j in range(self.cols):
                val = self.data[i][j]
                self.data[i][j] = function(val)

    def static_map(self, matrix, function):
        result = Matrix(matrix.rows, matrix.cols)
        for i in range(matrix.rows):
            for j in range(matrix.cols):
                val = matrix.data[i][j]
                result.data[i][j] = function(val)
        return result

    # Multiply Matrices
    def static_multiply(self, a, b):
        if a.cols != b.rows:
            print('Array Invalid')
            raise ValueError
        else:  # Multiplying other Matrix
            result = Matrix(a.rows, b.cols)
            for i in range(result.rows):
                for j in range(result.cols):
                    sum = 0
                    for k in range(a.cols):  
                        sum += a.data[i][k] * b.data[k][j]
                    result.data[i][j] = sum
            return result