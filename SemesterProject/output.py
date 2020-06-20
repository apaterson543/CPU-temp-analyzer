import os
import errno


class Outputs:
    def data_to_file(self, xk, xk1, y_num, c0, c1, calc_type, filename):
        filename.write(str(xk) + ' <= x < ' + str(xk1) + '; y_' + str(y_num) +
                       '   =   ' + str(c0) + ' + ' + str(c1) + 'x; ' + calc_type + '\n')
        # print(xk, ' <= x < ', xk1, '; y_', y_num,
        #       '   =   ', c0, ' + ', c1, 'x; ', calc_type)

    def create_directory(self, dir_name):
        la_directory = "./outputfiles/" + dir_name
        if not os.path.exists(os.path.dirname(la_directory)):
            try:
                os.makedirs(os.path.dirname(la_directory))
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise
