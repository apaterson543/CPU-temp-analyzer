
class MatrixOperations:
    """
    This class consists of operations that can be done on matrices
    """
    def check_compatibility(self, a, b):
        """
        Not yet implemented
        """
        # Check to see if matricies are compatible for these functions
        return self

    def transpose(self, x):
        """
        This function will transpose a nxn matrix

        :param x: the matrix before transposition input as a 2d list

        :yields: a transposed version of x
        """
        xt = [[row[i] for row in x] for i in range(len(x[0]))]
        return xt

    def multiply(self, a, b):
        """
        This function will multiply two matrices that are compatible.
        For the purpose of this project, compatibility has not yet been implemented.

        :param a: first matrix
        :param b: second matrix

        :yields: product matrix 'c'
        """
        c = []
        # self.check_compatibility(a ,b)
        for i in range(0, len(a)):
            new = []
            for j in range(0, len(b[0])):
                new.append(0)
            c.append(new)
        for i in range(len(c)):
            for j in range(len(c[0])):
                for k in range(len(a[0])):
                    c[i][j] += a[i][k] * b[k][j]

        return c

    def augment(self, x, y):
        """
        Will combine a nxn matrix with a compatible vector to form an augmented matrix

        :param x: the nxn matrix
        :param y: the vector that height of n

        :yields: an augmented matrix
        """

        # self.check_compatibility(a ,b)

        xtx_xty = x
        for i in range(len(xtx_xty)):
            xtx_xty[i].append(y[i][0])

        return xtx_xty

    def reduce_matrix(self, m):
        """
        This function uses gauss-jordan elimination to reduce an augmented matrix into an identity matrix

        :param m: The augmented matrix input for reduction
        """
        # Reduce matrix to upper echelon form
        for i in range(len(m)):
            if m[i][i] is 0:
                c = 1
                while (i + c < len(m)) and (m[i + c][i] == 0):
                    c += 1
                if (i + c) is len(m):
                    break
                for k in range(len(m)):
                    m[i][k], m[i + c][k] = m[i + c][k], m[i][k]

            for j in range(len(m)):
                if i is not j:
                    p = m[j][i] / m[i][i]
                    for k in range(len(m[i])):
                        m[j][k] -= m[i][k] * p

        # Reduce upper right matrix to identity matrix
        leading = 0
        for row in m:
            for i in range(len(row)):
                if row[i] != 0 and leading == 0:
                    leading = row[i]
                    row[i] = row[i] / leading
                elif row[i] != 0:
                    row[i] = row[i] / leading
            leading = 0

        # Return reduced matrix
        return m