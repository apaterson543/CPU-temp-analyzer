from output import Outputs
class PiecewiseInterpolation:

    """
    This class contains functions to calculate piecewise interpolation for
    individual cores based on data for CPU core temperatures at given times.
    """
    def interpolate(self, input_data):
        """
        Driver for interpolation and output of data to files
        :param input_data: Contains multiple columns. The first column is time,
                            the following are the readings for individual cores.

        :yields: Output files for each core that is processed.
        """
        # Create output object
        out = Outputs()
        # Core number that is being worked on. Starts at 1 because col0 is time.
        core_index = 1
        # Create directory for outputs if it does not already exist.
        out.create_directory("la_and_pi_files/")
        # Loop through all cores(columns) in input file
        for number_of_cores in range(1, len(input_data[0])):
            # Counter for index of time that holds core data. Resets upon new core.
            time_index = 0
            # Open output file for current core in created directory.
            pi_file_for_core = open(
                "./outputfiles/la_and_pi_files/core" + str(core_index - 1) + ".txt", "a")

            # Loop through all rows in input data and process interpolation for
            #   each increment
            for _ in input_data:
                # Collect x bounds(adjacent times)
                xs = self.get_x_bounds_from_time(input_data, time_index)
                # Collect y values at times(temperatures)
                ys = self.get_temps_as_y_vals(input_data, time_index, core_index)
                # If it as at the end of the list, xs or ys will return a flag
                if (xs is -1) or (ys is -1):
                    break
                # retrieve constant values for line equation
                pi_consts = self.get_line_equation_values(xs, ys)
                bi, mi = pi_consts[0], pi_consts[1]
                # Print equations to core specific file
                out.data_to_file(xs[0], xs[1], time_index, bi, mi, 'Piecewise Interpolation', pi_file_for_core)
                # Increment time_index to make sure next line in input data is being processed
                time_index += 1
            # Close core specific file
            pi_file_for_core.close()
            # Increment to move to next core
            core_index += 1
        print(" files saved in: './outputfiles/interpolationfiles/'")

    def get_x_bounds_from_time(self, data, index):
        """
        Get the adjacent times as x bounds

        :param data: the full input data
        :param index: row that is currently being processed from data

        :yields: tuple of xs or -1 if index is the end of the list
        """
        if (index + 1) < len(data):
            xs = [data[index][0], data[index + 1][0]]
            return xs
        else:
            return -1

    def get_temps_as_y_vals(self, data, index, core):
        """
        Get the vertically adjacent temps as y values

        :param data: the full input data
        :param index: row that is currently being processed from data
        :param core: column index of core being processed

        :yields: tuple of ys or -1 if index is the end of the list
        """
        if (index + 1) < len(data):
            ys = [data[index][core], data[index + 1][core]]
            return ys
        else:
            return -1

    def get_line_equation_values(self, x, y):
        """
        Calculates the b and m values for a y=mx+b line equation

        :param x: x tuple
        :param y: y tuple

        :yields: b and m values as a tuple
        """
        x0 = x[0]
        x1 = x[1]
        y0 = y[0]
        y1 = y[1]
        m = (y1-y0)/(x1 - x0)
        bi = y0 - (m * x0)
        p_consts = [bi, m]

        return p_consts