from matrixoperations import MatrixOperations
from output import Outputs

class LinearApproximation:
    # def __init__(self, xk, xk1, c0, c1, y_num, calc_type):
    #     self.x = []
    #     self.xk = xk
    #     self.xk1 = xk1
    #     self.c0 = c0
    #     self.c1 = c1
    #     self.y_num = y_num
    #     self.calc_type = calc_type

    def get_linear_approximation_as_files(self):
        return self

    def approximate(self, input_data):
        mat_ops = MatrixOperations()
        out = Outputs()
        # for row in range(len(input_data)):
        core_index = 1
        # for loop
        for number_of_cores in range(1, len(input_data[0])):
            time_index = 0
            la_file_for_core = open("core" + str(core_index - 1) + "_approximations.txt'", "w+")
            for row in input_data:
                # Create matrix 'X'
                x = self.create_matrix_x(input_data, time_index)
                # Create vector 'Y'
                y = self.create_matrix_y(input_data, time_index, core_index)
                # Create augmented matrix 'XTX|XTY'
                if (x is -1) or (y is -1):
                    break

                augmented = self.form_xtx_xty(x, y, mat_ops)
                reduced = mat_ops.reduce_matrix(augmented)

                xk = row[0]
                xk1 = xk + 30
                c0 = reduced[0][2]
                c1 = reduced[1][2]
                y_num = time_index
                calc_type = 'Linear Approximation'

                out.data_to_file(xk, xk1, y_num, c0, c1, calc_type, core_index, la_file_for_core)

                time_index += 1
            la_file_for_core.close()
            core_index += 1

    def create_matrix_x(self, all_data, index):
        if (index + 1) < len(all_data):
            x = [[1, float(all_data[index][0])], [1, float(all_data[index + 1][0])]]
            return x
        else:
            return -1

    def create_matrix_y(self, all_data, index, core):
        if (index + 1) < len(all_data):
            y = [[float(all_data[index][core])], [float(all_data[index + 1][core])]]
            return y
        else:
            return -1

    def form_xtx_xty(self, x, y, mat_ops):
        xt = mat_ops.transpose(x)
        xtx = mat_ops.multiply(xt, x)
        xty = mat_ops.multiply(xt, y)
        xtx_xty = mat_ops.augment(xtx, xty)
        return xtx_xty

    def create_files(self):
        # loop through each column of core approximations
        return self


