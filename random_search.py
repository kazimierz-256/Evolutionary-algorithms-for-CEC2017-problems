import numpy as np

import config
import util
import wrapper
from single_evaluation import SingleEvaluation


def run_and_compare_to_random(fn_id, se, random_o, ff, f_o):
    se.optimize_min()
    rand_v, rand_bv = random_o.get_results()
    print('random best:', (rand_bv[fn_id][-1]))
    print('random best error:', rand_bv[fn_id][-1] / (fn_id * 100))

    ff.optimize_min()
    v, bv = f_o.get_results()
    print('f best:', (bv[fn_id][-1]))
    print('f best error:', bv[fn_id][-1] / (fn_id * 100))
    util.plot_results(fn_id, rand_v, rand_bv, v, bv,
                      config.filename_prefix + str(fn_id) + '.png')


def main():
    import time
    np.random.seed(1)

    limit = config.limit
    initial_sample_count = 40

    tt = time.time()

    dim = 10
    random_o = wrapper.O(config.get_filename_prefix(algo_name='random'))

    o = wrapper.O(config.get_filename_prefix())

    for i in range(1, 11):
        print('Function', i)
        if config.algo == config.DIFF:

            se = SingleEvaluation(dim=dim, limit=limit, cec2017=random_o.cec2017, fn_id=i)

            from differential_evolution import DifferentialEvolution

            mu = 10
            de = DifferentialEvolution(10, limit=limit, mu=mu, cec2017=o.cec2017, fn_id=i)
            run_and_compare_to_random(i, se, random_o, de, o)

        elif config.algo == config.RAND:
            se = SingleEvaluation(dim=dim, limit=limit, cec2017=random_o.cec2017, fn_id=i)
            se.optimize_min()
        elif config.algo == config.LIPOLD:
            se = SingleEvaluation(dim=dim, limit=limit, cec2017=random_o.cec2017, fn_id=i)

            from lipold import LipoLD

            lild = LipoLD(o.cec2017, fn_number=i, dim=dim, limit=limit, initial_sample_count=initial_sample_count,
                          population_size=1000,
                          population_size_global=0, break_when_found_good_estimate=False)

            run_and_compare_to_random(i, se, random_o, lild, o)
        elif config.algo == config.COMPACTOR:
            se = SingleEvaluation(dim=dim, limit=limit, cec2017=random_o.cec2017, fn_id=i)

            from compactor import Compactor
            survival_rate = .9
            probes_per_iteration = 100
            print('Expected accuracy (euclidean distance) is about',
                  survival_rate ** (limit / (probes_per_iteration * dim)))
            cpctr = Compactor(o.cec2017, fn_number=i, dim=dim, limit=limit, survival_rate=survival_rate,
                              probes_per_iteration=probes_per_iteration, safety_closeness_to_past=0.5)
            cpctr.optimize_min()
            run_and_compare_to_random(i, se, random_o, cpctr, o)

    print('time elapsed:', time.time() - tt)
    o.save_results()


if __name__ == "__main__":
    main()
