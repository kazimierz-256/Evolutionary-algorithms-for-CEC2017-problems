import numpy as np

import config
import util
import wrapper
from single_evaluation import SingleEvaluation


def run_and_compare_to_random(fn_id, se, random_o, ff, f_o):
    se.optimize_min()
    rand_v, rand_bv = random_o.get_results()
    print('random best {0:E}'.format(rand_bv[fn_id][-1]))
    print('random best error {0:E}'.format(rand_bv[fn_id][-1] / (fn_id * 100)))

    ff.optimize_min()
    v, bv = f_o.get_results()
    print('f best {0:E}'.format(bv[fn_id][-1]))
    print('f best error {0:E}'.format(bv[fn_id][-1] / (fn_id * 100)))
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
            de = DifferentialEvolution(dim=10, limit=limit, mu=mu, cec2017=o.cec2017, fn_id=i)
            run_and_compare_to_random(fn_id=i, se=se, random_o=random_o, ff=de, f_o=o)
        elif config.algo == config.RAND:
            se = SingleEvaluation(dim=dim, limit=limit, cec2017=random_o.cec2017, fn_id=i)
            se.optimize_min()
        elif config.algo == config.LIPOLD:
            se = SingleEvaluation(dim=dim, limit=limit, cec2017=random_o.cec2017, fn_id=i)

            from lipold import LipoLD

            lild = LipoLD(cec2017=o.cec2017, fn_number=i, dim=dim, limit=limit,
                          initial_sample_count=initial_sample_count,
                          population_size=1000,
                          population_size_global=0, break_when_found_good_estimate=False)

            run_and_compare_to_random(fn_id=i, se=se, random_o=random_o, ff=lild, f_o=o)
        elif config.algo == config.COMPACTOR:
            se = SingleEvaluation(dim=dim, limit=limit, cec2017=random_o.cec2017, fn_id=i)

            from compactor import Compactor
            survival_rate = .9
            probes_per_iteration = 100
            print('Expected accuracy (euclidean distance) is about',
                  survival_rate ** (limit / (probes_per_iteration * dim)))
            cpctr = Compactor(o.cec2017, fn_number=i, dim=dim, limit=limit, survival_rate=survival_rate,
                              probes_per_iteration=probes_per_iteration, safety_closeness_to_past=0.5)

            run_and_compare_to_random(fn_id=i, se=se, random_o=random_o, ff=cpctr, f_o=o)
        elif config.algo == config.SUBSPYCE:
            se = SingleEvaluation(dim=dim, limit=limit, cec2017=random_o.cec2017, fn_id=i)

            from subsp import Subspyce
            probes_per_dimension = lambda dimension: dimension
            initial_probe_count = int(limit / 10)
            sbspc = Subspyce(cec2017=o.cec2017, fn_number=i, dim=dim, limit=limit,
                             probes_per_dimension=probes_per_dimension,
                             min_dim=10, max_dim=10, initial_probe_count=initial_probe_count)

            run_and_compare_to_random(fn_id=i, se=se, random_o=random_o, ff=sbspc, f_o=o)

    print('time elapsed:', time.time() - tt)
    o.save_results()


if __name__ == "__main__":
    main()
