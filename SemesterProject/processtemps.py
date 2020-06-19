import sys
import re
from matrixoperations import MatrixOperations
from linearapproximation import LinearApproximation

# Test matricies for initial qauss jordan elimination
data = [[0, 0],
        [1, 1],
        [2, 4]]

X = [[3, 3, 4, 0],
     [3, 5, 9, 0],
     [5, 9, 17, 0],
     [0, 0, 0, 4]]

Y = [[5],
     [9],
     [17],
     [4]]


class ProcessedOutput:
    def __init__(self, core_number, xk, xk_plus_one, yi, c0, c1, proc_type):
        self.core_number = core_number
        self.xk = xk
        self.xk_plus_one = xk_plus_one
        self.yi = yi
        self.c0 = c0
        self.c1 = c1
        self.proc_type = proc_type

    # def __repr__(self):
    #     return "Time:% s core 0:% s core 1:% s core 2:% s core 3:% s" % (self.time_in_seconds,
    #                                                                      self.core0,
    #                                                                      self.core1,
    #                                                                      self.core2,
    #                                                                      self.core3)


def parse_temps(line, time):
    temps_at_time = [time]
    for element in line.split():
        element = re.sub(r'[^\d.]+', '', element)
        temps_at_time.append(element)

    return temps_at_time


def read_temps(file):
    formatted_temps = []
    with open(file, 'r') as f:
        time = 0
        for line in f:
            temps_time = parse_temps(line, time)
            temps_time = [float(i) for i in temps_time]
            formatted_temps.append(temps_time)
            time += 30

    return formatted_temps


def process_single_core(core_readings):
    time = []
    x = []
    y = []
    xt = []
    xtx = []
    xty = []
    for temp in core_readings:
        x.append([1, temp])

    return x


def process_data(file, ctype):
    mat_ops = MatrixOperations()
    chart_of_temps = read_temps(file)
    linear_approx = LinearApproximation()

    linear_approx.approximate(chart_of_temps)
    # core_temps = []
    # for row in range(len(chart_of_temps)):
    #     core_temps.append(chart_of_temps[row][1])
    # x = process_single_core(core_temps)
    #
    # # Test output
    # # for line in x:
    # #     print(line)
    #
    # xt = mat_ops.transpose(X)
    # xtx = mat_ops.multiply(xt, X)
    # xty = mat_ops.multiply(xt, Y)
    # # augmented_matrix = mat_ops.augment(xtx, xty)
    # # augmented_matrix = mat_ops.augment(X,Y)
    #
    # # for line in augmented_matrix:
    # #     print(line)
    #
    # # cs = mat_ops.reduce_matrix(augmented_matrix)
    # # for line in cs:
    # #     print(line)


if __name__ == "__main__":
    # Input file with temperature data
    input_file = sys.argv[1]
    # Type of processing -- 1 for piecewise linear interpolation
    #                    -- 2 for global linear least squares approximation
    calculation_type = sys.argv[2]
    process_data(input_file, calculation_type)
