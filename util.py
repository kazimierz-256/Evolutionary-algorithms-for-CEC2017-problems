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


def plot_results_to_compare(fn_id, f_vals_rand, f_best_val_rand, f_vals, f_best_val, filename):
    import matplotlib.pyplot as plt
    vals_rand, b_vals_rand, vals, b_vals = f_vals_rand[fn_id], f_best_val_rand[fn_id], f_vals[fn_id], f_best_val[fn_id]

    if len(vals_rand) == 0:
        return
    plt.clf()
    fig = plt.figure()
    plt.axis([0, len(vals_rand), 0, (b_vals[-1]) * 4])
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(vals, color='b', label='f')
    ax.plot(b_vals, color='r', label='best_val')
    ax.plot(b_vals_rand, color='g', label='rand_best_val')
    fig.savefig(filename)
    plt.legend()
    plt.close()
    print("plot " + filename + ' saved')


def plot_results(fn_id, f_vals, f_best_val, filename):
    import matplotlib.pyplot as plt
    vals, b_vals = f_vals[fn_id], f_best_val[fn_id]

    if len(vals) == 0:
        return
    plt.clf()
    fig = plt.figure()
    plt.axis([0, len(vals), 0, (b_vals[-1]) * 4])
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(vals, color='b', label='f')
    ax.plot(b_vals, color='r', label='best_val')
    fig.savefig(filename)
    plt.legend()
    plt.close()
    print("plot " + filename + ' saved')
