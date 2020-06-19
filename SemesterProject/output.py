class Outputs:
    def data_to_file(self, xk, xk1, y_num, c0, c1, calc_type, core_number, filename):
        filename.write(str(xk) + ' <= x < ' + str(xk1) + '; y_' + str(y_num) +
                       '   =   ' + str(c0) + ' + ' + str(c1) + 'x; ' + calc_type + '\n')
        print(xk, ' <= x < ', xk1, '; y_', y_num,
              '   =   ', c0, ' + ', c1, 'x; ', calc_type)
