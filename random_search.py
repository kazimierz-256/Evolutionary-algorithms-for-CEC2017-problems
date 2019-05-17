from math import ceil

import numpy as np

from wrapper import cec2017, init, save_results


def single_evaluation(i, n):
    #best_result = cec2017(i, np.random.rand(1, n))
    for k in range(1000):
        x = np.random.rand(1, n)
        result = cec2017(i, x)
    return


if __name__ == "__main__":
    init("Test_rand")
    for i in range(1, 10):
        single_evaluation(i, 10)
    save_results()
