from matrixoperations import MatrixOperations
from output import Outputs


class CubicSpline:
    """
    This class generates piecewise cubic spline equations for temperatures between time x0 and xk
    """

    def generate_spline(self, input_data):
        """
        Main driver for generating cubic splines and prints them out by individual core

        :param input_data: The 2d list of data containing individual core temperatures at
                            given times

        :yields: Output file for each core in designated folder.
        """

        # Create output object
        out = Outputs()
        # Core number that is being worked on. Starts at 1 because col0 is time.
        core_index = 1
        # Create directory for outputs if it does not already exist.
        out.create_directory("splinefiles/")
        # Loop through all cores(columns) in input file
        for number_of_cores in range(1, len(input_data[0])):
            # Counter for index of time that holds core data. Resets upon new core.
            time_index = 0
            # Open output file for current core in created directory.
            cs_file_for_core = open(
                "./outputfiles/splinefiles/core" + str(core_index - 1) + "_splines.txt", "a")

            # Loop through all rows in input data and process interpolation for
            #   each increment
            for _ in input_data:
                # Collect x bounds(adjacent times)
                x_vals = self.get_times_as_x_vals(input_data, time_index)
                # Collect y values at times(temperatures)
                f_vals = self.get_vector_vals_for_i(input_data, time_index, core_index)
                # If it as at the end of the list, xs or ys will return a flag
                if (x_vals is -1) or (f_vals is -1):
                    break
                # retrieve constant values for line equation
                vect_vals = self.get_right_col_vals(x_vals, f_vals)
                reduced = self.create_matrix_and_solve(vect_vals)

                cs = self.get_cs_from_ms(reduced, f_vals, x_vals)
                # Print equations to core specific file
                out.splines_to_file(x_vals[0], x_vals[2], time_index, cs, 'Cubic Spline', cs_file_for_core)
                # Increment time_index to make sure next line in input data is being processed
                time_index += 1
            # Close core specific file
            cs_file_for_core.close()
            # Increment to move to next core
            core_index += 1
        print(" files saved in: 'SemesterProject/outputfiles/splinefiles/'")

    def get_times_as_x_vals(self, data, index):
        """
        Get the adjacent times as x bounds

        :param data: the full input data
        :param index: row that is currently being processed from data

        :yields: triple of xs or -1 if index is the end of the list
        """
        if (index + 2) < len(data):
            xs = [data[index][0], data[index + 1][0], data[index + 2][0]]
            return xs
        else:
            return -1

    def get_vector_vals_for_i(self, data, index, core):
        """
        Get the vertically adjacent temps as y values

        :param data: the full input data
        :param index: row that is currently being processed from data
        :param core: column index of core being processed

        :yields: triple of fs or -1 if index is the end of the list
        """
        if (index + 2) < len(data):
            ys = [data[index][core], data[index + 1][core], data[index + 2][core]]
            return ys
        else:
            return -1

    def get_right_col_vals(self, xs, fs):
        vect = []

        delta_x2, delta_x3 = self.get_differences(xs)
        f1, f2 = self.get_f_for_set(fs, delta_x2, delta_x3)
        vect.append([3 * f1])
        vect.append([3 * (f1 + f2)])
        vect.append([3 * f2])
        return vect

    def get_differences(self, xs):
        delta_x2 = xs[1] - xs[0]
        delta_x3 = xs[2] - xs[1]

        return delta_x2, delta_x3

    def get_f_for_set(self, fs, delta_x2, delta_x3):
        f1 = (fs[1] - fs[0]) / delta_x2
        f2 = (fs[1] - fs[2]) / delta_x3
        return f1, f2

    def create_matrix_and_solve(self, vect_vals):
        matops = MatrixOperations()
        m_vals = [[2, 1, 0],
                  [1, 4, 1],
                  [0, 1, 2]]
        augmented = matops.augment(m_vals, vect_vals)
        reduced = matops.reduce_matrix(augmented)
        return reduced

    def get_cs_from_ms(self, matrix, f_vals, x_vals):
        c_vals = []

        m1 = matrix[0][3]
        m2 = matrix[1][3]
        m3 = matrix[2][3]
        delta_x2, delta_x3 = self.get_differences(x_vals)
        f1, f2 = self.get_f_for_set(f_vals, delta_x2, delta_x3)
        delta_xi = delta_x2+delta_x3
        c10 = f_vals[0]
        c1r = m1
        c13 = (m2+m1-(2*f1))/(delta_xi * delta_xi)
        c12 = ((f1 - m1)/delta_xi) - (c13*delta_xi)

        c_vals.append(c10)
        c_vals.append(c1r)
        c_vals.append(c12)
        c_vals.append(c13)

        return c_vals
