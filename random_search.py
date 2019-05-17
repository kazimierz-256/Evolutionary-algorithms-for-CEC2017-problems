import numpy as np

import config
import util
from wrapper import init, save_results


def single_evaluation(i, n, limit, cec2017):
    for _ in range(limit):
        x = np.random.rand(1, n) * 200 - 100
        _ = cec2017(i, x)[0]


def main():
    import time
    np.random.seed(1)

    limit = 1000
    initial_sample_count = 40
    init(config.filename_prefix + str(limit))

    tt = time.time()

    dim = 10
    import wrapper
    o = wrapper.O()
    cec2017 = o.cec2017
    for i in range(1, 11):
        print('Function', i)
        if config.algo == config.DIFF:
            from differential_evolution import differential_evolution

            differential_evolution(i, 10, limit=limit, mu=10)
        elif config.algo == config.RAND:
            single_evaluation(i, dim, limit)
        elif config.algo == config.LIPOLD:
            from lipold import LipoLD
            single_evaluation(i, dim, limit, cec2017)
            rand_v, rand_bv = o.get_results()
            o.clear_results()

            lild = LipoLD(cec2017, fn_number=i, dim=dim, limit=limit, initial_sample_count=initial_sample_count,
                          population_size=1000,
                          population_size_global=0, break_when_found_good_estimate=False)
            lild.optimize_min()

            v, bv = o.get_results()
            o.clear_results()
            util.plot_results(rand_v, rand_bv, v, bv, config.filename_prefix + str(i) + '.png')

    print('time elapsed:', time.time() - tt)
    save_results()


if __name__ == "__main__":
    main()
