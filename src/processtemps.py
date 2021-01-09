import sys
import re

from linearapproximation import LinearApproximation
from piecewiseinterpolation import PiecewiseInterpolation
from cubicspline import CubicSpline
class ProcessTemps:

    def parse_temps(self, line, time):
        """
        Parse temperatures from file using regex to eliminate non-float values

        :param line: line in input file
        :param time: add time (increments of 30) to a new column in front of core0
                     readings

        :yields: list of temps as floats for line
        """
        temps_at_time = [time]
        for element in line.split():
            # Remove any char that is not a number or a '.'
            element = re.sub(r'[^\d.]+', '', element)
            temps_at_time.append(element)

        return temps_at_time

    def read_temps(self, file):
        """
        Reads temperatures line by line from input file

        :param file: input filepath

        :yields: list of all temperatures with time in rows with elements in
                 the order:
                    temp core0 core1 core2 ... coreN
        """
        formatted_temps = []
        with open(file, 'r') as f:
            time = 0
            for line in f:
                temps_time = self.parse_temps(line, time)
                temps_time = [float(i) for i in temps_time]
                formatted_temps.append(temps_time)
                time += 30

        return formatted_temps

    def process_data(self, file, ctype):
        """
        Driver:
            Collect information from input file. Input file filepath should be the first
            command line argument followed by the The type of calculation you wish to perform:

                1: Global Linear Approximation
                2: Piecewise Interpolation
                3: Cubic Spline

            This function sends the data from the input file to be proccessed ito a usable form
            then sends it off to its respective processing sector of this program.

            :param file: The input file that consists of cpu temperatures
            :param ctype: the command line argument for the calculation type to be performed

            Files are saved to SemesterProject/outputfiles/ on creation


        """
        # 2D list of temps at times
        chart_of_temps = self.read_temps(file)

        if ctype is '1':
            print("Calculating global linear approximation...")
            linear_approx = LinearApproximation()
            linear_approx.approximate(chart_of_temps)
            print("Done.")

        elif ctype is '2':
            print("Calculating piecewise interpolations...")
            piecewise_interpolation = PiecewiseInterpolation()
            piecewise_interpolation.interpolate(chart_of_temps)
            print("Done.")

        elif ctype is '3':
            print("Calculating cubic splines...")
            cubic_spline = CubicSpline()
            cubic_spline.generate_spline(chart_of_temps)
            print("Done.")

        elif ctype is '4':
            print("All calculations processing...")
            linear_approx = LinearApproximation()
            piecewise_interpolation = PiecewiseInterpolation()
            cubic_spline = CubicSpline()
            print("Calculating global linear approximation...")
            linear_approx.approximate(chart_of_temps)
            print("Calculating piecewise interpolations...")
            piecewise_interpolation.interpolate(chart_of_temps)
            print("Calculating Cubic Spines...")
            cubic_spline.generate_spline(chart_of_temps)
            print("Done.")

        else:
            print("ERROR: Please retry execution with valid arguments:")
            print("       'python3 processtemps.py testfilepath #' ")
            print("        where '#' is one of the following: ")
            print("         1 -> Global Linear Approximation")
            print("         2 -> Piecewise Interpolation")
            print("         3 -> Cubic Spline")
            print("         4 -> Perform All Of The Above")


if __name__ == "__main__":
    # Input file with temperature data
    input_file = sys.argv[1]
    process_temps = ProcessTemps()
    # Type of processing -- 1 for piecewise linear interpolation
    #                    -- 2 for global linear least squares approximation
    calculation_type = sys.argv[2]
    process_temps.process_data(input_file, calculation_type)