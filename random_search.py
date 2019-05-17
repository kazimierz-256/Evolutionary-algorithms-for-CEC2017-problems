import numpy as np

import config
from wrapper import cec2017, init, save_results, plot_results


def single_evaluation(i, n, limit):
    # best_result = cec2017(i, np.random.rand(1, n))
    for _ in range(limit):
        x = np.random.rand(1, n) * 200 - 100
        f = cec2017(i, x)[0]
        # print("f: ", f, 'i', i)
    return


if __name__ == "__main__":
    import time

    np.random.seed(1)

    dim = 10

    limit = 100
    init(config.filename_prefix + str(limit))

    tt = time.time()


    def exploration_cdf(t):
        if t < 2:  # limit/2:
            return 1.
        else:
            return 0


    for i in range(1, 11):
        if config.algo == config.DIFF:

            from differential_evolution import differential_evolution

            differential_evolution(i, 10, limit=limit, mu=10)
        elif config.algo == config.RAND:
            single_evaluation(i, dim, limit)
    print('time elapsed:', time.time() - tt)
    save_results()
    plot_results()
