import os
import errno


class Outputs:
    def data_to_file(self, xk, xk1, y_num, c0, c1, calc_type, filename):
            filename.write('{:7}'.format(str(xk)) + '{:>7}'.format(' <= x < ') + '{:>7}'.format(str(xk1)) + '; y_' + '{:3}'.format(str(y_num)) +
                           '{:7}'.format('   =   ') + '{:>10}'.format('{:.2f}'.format(c0)) + '{:6}'.format(' + ') + '{:>10}'.format('{:f}'.format(c1)) + 'x; ' + calc_type + '\n')


    def create_directory(self, dir_name):
        la_directory = "./outputfiles/" + dir_name
        if not os.path.exists(os.path.dirname(la_directory)):
            try:
                os.makedirs(os.path.dirname(la_directory))
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise

    def splines_to_file(self, xk, xk2, y_num, cs, calc_type, filename):
        filename.write('{:7}'.format(str(xk)) + '{:>7}'.format(' <= x < ') + '{:>7}'.format(str(xk2)) + '; y_' + '{:3}'.format(str(y_num)) +
                       '{:>7}'.format('   =   ' + str(cs[0])) + ' +' + '{:>10}'.format('{:f}'.format(cs[1])) + 'x  +' +
                       '{:>15}'.format('{:f}'.format(cs[2])) + 'x^2  +' + '{:>10}'.format('{:f}'.format(cs[3])) + 'x^3; ' + calc_type + '\n')