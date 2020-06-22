from matrixoperations import MatrixOperations
from output import Outputs


class LinearApproximation:
    """
    This class generates either a global linear approximation between time_0 and time_k
    or
    individual linear approximations between time_n and time_n+1 from time_0 to time_k
    """

    def approximate(self, input_data):
        """
        Main driver for approximate. Calls necessary functions to create a global
            linear approximation set for individual cores

        :param input_data: The 2d list of data containing individual core temperatures at
                            given times

        :yields: Output file for each core in designated folder.
        """
        # Create Output object
        out = Outputs()
        # Core number that is being worked on. Starts at 1 because col0 is time.
        core_index = 1
        # Loop through all cores(columns) in input file
        for number_of_cores in range(1, len(input_data[0])):
            # Counter for index of time that holds core data. Resets upon new core.
            time_index = 0

            out.create_directory('la_and_pi_files/')
            la_file_for_core = open("./outputfiles/la_and_pi_files/core"
                    + str(core_index - 1) + ".txt", "a")
            # Do necessary operations on input data to gain a reduced augmented matrix
            reduced = self.process_global_approximation(input_data, core_index)
            # Output calculated information
            self.print_approximations_to_file(out, len(input_data), reduced, time_index, 2, la_file_for_core)
            # Increment to next core (column)
            core_index += 1
            la_file_for_core.close()

        print(" files saved in: './outputfiles/la_and_pi_files/'")

    def create_x_matrix(self, data):
        """
        Creates X matrix based on all time values. Used for global approximations

        :param data: full data set as list

        :yields: X matrix
        """
        x = []
        for temp in range(len(data)):
            x.append([1, data[temp][0]])
        return x

    def create_y_matrix(self, data, core):
        """
        Creates Y vector based on all temp values for core. Used for global approximations

        :param data: full data set as list

        :yields: Y vector
        """
        y = []
        for line in range(len(data)):
            y.append([data[line][core]])
        return y

    def form_xtx_xty(self, x, y, mat_ops):
        """
        Transposes X, then multiplies Xt * X and Xt * Y.
        Then combines them to form an augmented matrix.

        :param x: X matrix
        :param y: Y vector
        :param mat_ops: MatrixOperations class object. Aids in utilization of matrix operations.

        :yields: augmented XTX|XTY matrix
        """
        xt = mat_ops.transpose(x)
        xtx = mat_ops.multiply(xt, x)
        xty = mat_ops.multiply(xt, y)
        xtx_xty = mat_ops.augment(xtx, xty)

        return xtx_xty

    def process_global_approximation(self, input_data, core_index):
        """
        Processes all data for individual core at once. Creates matricies, augments and reduces.

        :param input_data: data list input
        :param core_index: column index of core being processed

        :yields: reduced augmented matrix as list
        """
        mat_ops = MatrixOperations()
        x = self.create_x_matrix(input_data)
        y = self.create_y_matrix(input_data, core_index)
        augmented = self.form_xtx_xty(x, y, mat_ops)
        reduced = mat_ops.reduce_matrix(augmented)

        return reduced

    def print_approximations_to_file(self, out, row, reduced, time_index, c_type, filepath):
        """
        Sends information in proper order to Ouput class to print the data to a file

        :param out: Output class object
        :param row: if called for individual approximations -> row index being processed
                    if called for global approximation      -> index of last row

        :param reduced: reduced augmented matrix as list
        :param time_index: index of time
        :param c_type: calculation type -> individual or global
        :param filepath: path of file to which to print

        :yields: data appended to specified file
        """
        if c_type is 1:
            xk = row[0]
            xk1 = xk + 30
        else:
            xk = 0
            xk1 = row
        c0 = reduced[0][2]
        c1 = reduced[1][2]
        y_num = time_index
        calc_type = 'Linear Approximation'

        out.data_to_file(xk, xk1, y_num, c0, c1, calc_type, filepath)
