from math import ceil

import numpy as np

from wrapper import cec2017, init, save_results


def differential_evolution(functionid, dim, limit, mu):
    def add_noise(x):
        return np.random.multivariate_normal(x, np.identity(dim) * (2 ** -20))

    points = [np.zeros(dim)]*mu #pewnie trzeba będzie w pewnym momencie to transponować
    fvalues = [0.0]*mu

    history = list()
    t = 0

    for i in range(mu):
            points[i] = np.random.multivariate_normal(np.zeros(dim), np.identity(dim) * 100)

    while t < limit:
        for i in range(mu):
            Pj = points[np.random.choice(len(points))]
            Pk = points[np.random.choice(len(points))]
            Pl = points[np.random.choice(len(points))]
            F = np.random.uniform(0, 1)
            new_point = add_noise(Pj + F * (Pk - Pl))
            # print('oaoa',new_point)
            evaluated = cec2017(functionid, new_point.T)
            if evaluated is not None:
                evaluated = evaluated[0]
            else:
                print('none tu', functionid, i)
            history.append((new_point, evaluated))
            t = t + 1
            if evaluated < fvalues[i]:
                points[i] = new_point
                fvalues[i] = evaluated


def single_evaluation(i, n):
    #best_result = cec2017(i, np.random.rand(1, n))
    for k in range(1000):
        x = np.random.rand(1, n)
        result = cec2017(i, x)
    return


if __name__ == "__main__":
    init("Test_rand")
    for i in range(1, 10):
        differential_evolution(i, 10, 100, 1000)
    save_results()
