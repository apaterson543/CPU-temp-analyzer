from matrixoperations import MatrixOperations
from output import Outputs


class LinearApproximation:
    """
    This class generates either a global linear approximation between time_0 and time_k
    or
    individual linear approximations between time_n and time_n+1 from time_0 to time_k
    """

    def approximate(self, input_data, calc_type):
        """
        Main driver for approximate. Calls necessary functions to create either global or
        piecewise linear approximation set for individual cores

        :param input_data: The list of data containing individual core temperatures at
                            given times
        :param calc_type: Determinant for whether a global or list of individual linear
                            approximations are calculated for the given core data

        :yields: Output file for each core in designated folder.
        """
        # Create Output object
        out = Outputs()
        # Core number that is being worked on. Starts at 1 because col0 is time.
        core_index = 1
        # Create directory for outputs if it does not already exist.
        out.create_directory("approximationfiles/")

        # Loop through all cores(columns) in input file
        for number_of_cores in range(1, len(input_data[0])):
            # Counter for index of time that holds core data. Resets upon new core.
            time_index = 0
            # If calc_type is 1, do individual approximations.
            if calc_type is 1:
                # Create designated directory for individual approximations.
                out.create_directory('approximationfiles/indiv_approx_files/')
                # Cpen file for specific core being processed.
                la_file_for_core = open(
                    "./outputfiles/approximationfiles/indiv_approx_files/core"
                    + str(core_index - 1) + "_approximations.txt'", "w+")

                # Loop through all rows processing vertically adjacent data
                for row in input_data:
                    # Do the necessary operations on input data to gain a reduced augmented matrix
                    reduced = self.process_individual_approximations(input_data, time_index, core_index)
                    # Check if end of data
                    if reduced is -1:
                        break
                    # Ouput calculated information
                    self.print_approximations_to_file(out, row, reduced, time_index, 1, la_file_for_core)
                    # Increment by row
                    time_index += 1

            # If calc_type is 2, perform a global linear interpolation
            else:
                out.create_directory('approximationfiles/global_approx_files/')
                la_file_for_core = open(
                    "./outputfiles/approximationfiles/global_approx_files/core"
                    + str(core_index - 1) + "_approximations.txt'", "w+")
                # Do necessary operations on input data to gain a reduced augmented matrix
                reduced = self.process_global_approximation(input_data, core_index)
                # Output calculated information
                self.print_approximations_to_file(out, len(input_data), reduced, time_index, 2, la_file_for_core)
            # Increment to next core (column)
            core_index += 1
            la_file_for_core.close()

        # Display directory locations of saved files to user
        if calc_type is 1:
            print(" files saved in: './outputfiles/approximationfiles/indiv_approx_files/'")
        else:
            print(" files saved in: './outputfiles/approximationfiles/global_approx_files/'")

    def get_times_as_x(self, all_data, index):
        """
        Get x bounds as a tuple. Used for individual pair approximations.

        :param all_data: full data set as list
        :param index: row in all_data that is currently being processed

        :yields: 2x2 X matrix or -1 for end of all_data
        """
        if (index + 1) < len(all_data):
            x = [[1, all_data[index][0]], [1, all_data[index + 1][0]]]
            return x
        else:
            return -1

    def get_core_temps_as_y(self, all_data, index, core):
        """
        Get adjacent temperatures of designated core at given index(time index).
            Used for individual pair approximations

        :param all_data: full data set as list
        :param index: row in all_data that is currently being processed
        :param core: column index in all_data of core being processed

        :yields: Y vector or -1 for end of all_data
        """
        if (index + 1) < len(all_data):
            y = [[all_data[index][core]], [all_data[index + 1][core]]]
            return y
        else:
            return -1

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

    def process_individual_approximations(self, input_data, time_index, core_index):
        """
        Processes pairs of lines in data. Creates matricies, augments and reduces.

        :param input_data: data list input
        :param time_index: row corresponding with time being processed
        :param core_index: column index of core being processed

        :yields: reduced augmented matrix as list
        """
        mat_ops = MatrixOperations()
        # Create matrix 'X'
        x = self.get_times_as_x(input_data, time_index)
        # Create vector 'Y'
        y = self.get_core_temps_as_y(input_data, time_index, core_index)

        # Create augmented matrix 'XTX|XTY'
        if (x is -1) or (y is -1):
            return -1

        augmented = self.form_xtx_xty(x, y, mat_ops)
        reduced = mat_ops.reduce_matrix(augmented)

        return reduced

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
