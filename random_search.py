import numpy as np

import config
import util

results_filename = 'out/results_dist.txt'


def run_and_compare(fn_id, se, random_o, ff, f_o):
    ff.optimize_min()
    v, bv = f_o.get_results()
    print('f best ', bv[fn_id][-1])
    # print('f best {0:E}'.format(bv[fn_id][-1]))
    # print('f best error {0:E}'.format(bv[fn_id][-1] / (fn_id * 100)))

    # se.optimize_min()
    # rand_v, rand_bv = random_o.get_results()
    # print('no_opt best ', rand_bv[fn_id][-1])
    # # print('random best {0:E}'.format(rand_bv[fn_id][-1]))
    # # print('random best error {0:E}'.format(rand_bv[fn_id][-1] / (fn_id * 100)))

    # with open(results_filename, 'a') as f:
    #     f.write(str(fn_id) + "\t" + str(bv[fn_id][-1]) + "\t" + str(rand_bv[fn_id][-1]) + "\n")

    with open(results_filename, 'a') as f:
        f.write(str(bv[fn_id][-1]) + "\n")

    # util.plot_results_to_compare(fn_id, rand_v, rand_bv, v, bv,
    #                              config.filename_prefix + str(fn_id) + '.svg')


def run_only(fn_id, ff, f_o):
    ff.optimize_min()
    v, bv = f_o.get_results()
    print('f best {0:E}'.format(bv[fn_id][-1]))
    print('f best error {0:E}'.format(bv[fn_id][-1] / (fn_id * 100)))
    util.plot_results(fn_id, v, bv,
                      config.filename_prefix + str(fn_id) + '.svg')


def main():
    import time
    from single_evaluation import SingleEvaluation
    from wrapper import O
    for seed in range(1, 10):
        with open(results_filename, 'a') as f:
            f.write("seed: " + str(seed) + "\n")
        np.random.seed(seed)

        limit = config.limit
        dim = config.dim

        tt = time.time()

        random_o = O(config.get_filename_prefix(algo_name='random'))
        o = O(config.get_filename_prefix())

        for i in range(1, 11):
            print('Function', i)
            if config.algo == config.DIFF:

                se = SingleEvaluation(dim=dim, limit=limit, cec2017=random_o.cec2017, fn_id=i)

                from differential_evolution import DifferentialEvolution

                mu = 10
                de = DifferentialEvolution(dim=10, limit=limit, mu=mu, cec2017=o.cec2017, fn_id=i)
                run_and_compare(fn_id=i, se=se, random_o=random_o, ff=de, f_o=o)
            elif config.algo == config.RAND:
                se = SingleEvaluation(dim=dim, limit=limit, cec2017=random_o.cec2017, fn_id=i)
                se.optimize_min()
            elif config.algo == config.LIPOLD:
                se = SingleEvaluation(dim=dim, limit=limit, cec2017=random_o.cec2017, fn_id=i)

                from lipold import LipoLD

                initial_sample_count = 40
                lild = LipoLD(cec2017=o.cec2017, fn_number=i, dim=dim, limit=limit,
                              initial_sample_count=initial_sample_count,
                              population_size=1000,
                              population_size_global=0, break_when_found_good_estimate=False)

                run_and_compare(fn_id=i, se=se, random_o=random_o, ff=lild, f_o=o)
            elif config.algo == config.COMPACTOR:
                se = SingleEvaluation(dim=dim, limit=limit, cec2017=random_o.cec2017, fn_id=i)

                from compactor import Compactor
                survival_rate = .9
                probes_per_iteration = 100
                print('Expected accuracy (euclidean distance) is about',
                      survival_rate ** (limit / (probes_per_iteration * dim)))
                cpctr = Compactor(o.cec2017, fn_number=i, dim=dim, limit=limit, survival_rate=survival_rate,
                                  probes_per_iteration=probes_per_iteration, safety_closeness_to_past=0.5)

                run_and_compare(fn_id=i, se=se, random_o=random_o, ff=cpctr, f_o=o)
            elif config.algo == config.SUBSPYCE:

                from subsp import Subspyce

                initial_probe_count = dim * 100
                no_opt = Subspyce(cec2017=random_o.cec2017, fn_number=i, dim=dim, limit=limit,
                                  initial_probe_count=initial_probe_count, local_optimization_iter=0)
                sbspc = Subspyce(cec2017=o.cec2017, fn_number=i, dim=dim, limit=limit,
                                 initial_probe_count=initial_probe_count, local_optimization_iter=20000)

                run_and_compare(fn_id=i, se=no_opt, random_o=random_o, ff=sbspc, f_o=o)

        print('time elapsed:', time.time() - tt)
    # o.save_results()


if __name__ == "__main__":
    main()
