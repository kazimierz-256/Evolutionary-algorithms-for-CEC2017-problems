# File cec2017.py
# Copyright 2018 Lukasz Neumann <fuine@riseup.net>
# Based on: https://CRAN.R-project.org/package=cec2017
# Distributed under GPL 3 or later

################################################################################
#                                 CEC 2017                                     #
################################################################################
# Purpose   : Evaluate a CEC-2017 benchamark function on a user-defined para-  #
#             meter set                                                        #
################################################################################
# i: integer in [1, 30], with the number of the CEC2017 benchmark function to  #
#    be evalauated                                                             #
# x: numeric, with the parameter set to be evaluated in the benchmark function #
#    Its length MUST be in [2, 10, 20, 30, 50, 100]                            #
################################################################################

# from src.utils import root_path
import os
import sys
from ctypes import cdll, c_double, c_int, POINTER, c_char_p

import numpy as np

c_double_p = POINTER(c_double)


class O:
    def __init__(self, results_file_name):
        self.f_vals = [[] for _ in range(30)]
        self.f_best_val = [[] for _ in range(30)]
        self.EVAL_LIMIT = 100000
        self.ITERATION = [0] * 30
        self.best_results = [sys.float_info.max] * 30
        self.results_file_name = results_file_name

    def save_results(self):
        with open(self.results_file_name, 'w') as f:
            for item in self.best_results:
                f.write("%s\n" % item)
        print("File saved")

    def get_results(self):
        from copy import copy
        return copy(self.f_vals), copy(self.f_best_val)

    def clear_results(self):
        self.f_vals = [[] for _ in range(30)]
        self.f_best_val = [[] for _ in range(30)]
        self.ITERATION = [0] * 30

    def cec2017(self, i, x):
        if self.EVAL_LIMIT - self.ITERATION[i] <= 0:
            return None
        self.ITERATION[i] = self.ITERATION[i] + 1
        assert isinstance(i, int)
        if i < 1 or i > 30:
            exit("Invalid argument: 'i' should be an integer between 1 and 30 !")

        try:
            sh = x.shape
        except AttributeError:
            exit("x must be a numpy array")
        if len(sh) == 1:
            row = 1
            col = sh[0]
        else:
            row = sh[0]
            col = sh[1]

        if col not in [2, 10, 20, 30, 50, 100]:
            exit("Invalid argument: Only 2, 10, 20, 30, 50 and 100 dimensions/variables are allowed !")

        path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                            "libcec2017C.so"))
        libc = cdll.LoadLibrary(path)
        cec2017 = libc.cec2017
        cec2017.argtypes = [c_char_p, c_int, c_double_p, c_int, c_int, c_double_p]

        x = x.astype(float, order='C')

        f = np.zeros(row)
        f = f.astype(float, order='C')

        cec2017(
            root_path("data", "cec2017").encode(),
            i,
            x.ctypes.data_as(c_double_p),
            row,
            col,
            f.ctypes.data_as(c_double_p))

        if self.best_results[i] > f:
            self.best_results[i] = f
            print("Hooray", self.best_results[i])

        self.f_vals[i].append(f[0])

        self.f_best_val[i].append(self.best_results[i][0])

        return f


def root_path(*args):
    """Get the path to the project root.

    Parameters
    ------
    args : List of args
        List of path elements e.g. ['data', 'data.csv']

    Returns
    -------
    path : str
        Absolute path to the resources folder.
    """
    path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.path.pardir))
    for item in args:
        path = os.path.abspath(os.path.join(path, item))

    return path


if __name__ == "__main__":
    o = O("test.txt")
    print(o.cec2017(1, np.zeros(50)))
