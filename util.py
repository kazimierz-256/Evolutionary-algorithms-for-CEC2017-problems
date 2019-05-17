import numpy as np


def crossover(vec1, vec2, prob=0.5):
    vec3 = np.copy(vec1)
    # print('a', len(vec1), 'b', len(vec2), 'c', vec3)
    for i, v in enumerate(vec2):
        if np.random.random() < prob:
            vec3[i] = v

    return vec3


def get_new_point(points, i, dim, do_crossover=False):
    def add_noise(x):
        return np.random.multivariate_normal(x, np.identity(dim) * (2 ** -20))

    def _get_random_element(l):
        return l[np.random.choice(len(l))][0]

    Pi = points[i][0]
    Pj = _get_random_element(points)
    Pk = _get_random_element(points)
    Pl = _get_random_element(points)
    F = np.random.uniform(0, 1)
    M = add_noise(Pj + F * (Pk - Pl))
    O = crossover(Pi, M)
    return O


def get_random_point_100(dim):
    return np.random.rand(dim) * 200 - 100


def plot_results(f_vals_rand, f_best_val_rand, f_vals, f_best_val, filename):
    import matplotlib.pyplot as plt
    for i, (vals_rand, b_vals_rand, vals, b_vals) in enumerate(zip(f_vals_rand, f_best_val_rand, f_vals, f_best_val)):
        if len(vals_rand) == 0:
            continue
        plt.clf()
        fig = plt.figure()
        plt.axis([0, len(vals_rand), 0, (b_vals[-1] + b_vals_rand[-1]) * 2])
        ax = fig.add_subplot(1, 1, 1)
        ax.plot(vals, color='b', label='f')
        ax.plot(b_vals, color='r', label='best_val')
        ax.plot(b_vals_rand, color='g', label='rand_best_val')
        fig.savefig(filename)
        plt.legend()
        plt.close()
        print("plot " + filename + ' saved')