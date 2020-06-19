class MatrixOperations:
    def __init__(self):
        self.mat = []

    def transpose(self, x):
        xt = [[row[i] for row in x] for i in range(len(x[0]))]
        return xt

    def multiply(self, a, b):
        c = []
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
        xtx_xty = x
        for i in range(len(xtx_xty)):
            xtx_xty[i].append(y[i][0])

        return xtx_xty

    def reduce_matrix(self, m):
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

        leading = 0
        for row in m:
            for i in range(len(row)):
                if row[i] != 0 and leading == 0:
                    leading = row[i]
                    row[i] = row[i] / leading
                elif row[i] != 0:
                    row[i] = row[i] / leading
            leading = 0

        return m
