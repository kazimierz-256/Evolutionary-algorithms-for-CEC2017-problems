import numpy as np


class Subspyce:
    def __init__(self, cec2017, fn_number, dim, limit, initial_probe_count, probability_table):
        self.dim = dim
        self.cec2017 = cec2017
        self.fn_number = fn_number
        self.limit = limit
        self.initial_probe_count = initial_probe_count
        self.probability_table = probability_table

    def optimize_min(self):
        available_samples = self.limit
        # probe the space
        sample_count = min(available_samples, self.initial_probe_count)
        available_samples -= sample_count
        samples = (np.random.uniform(size=self.dim) for _ in range(sample_count))

        # randomize initial set of points
        sample_fval_pairs = [(v, self.cec2017(self.fn_number, v)[0]) for v in samples]

        # choose the best one
        best = sample_fval_pairs[0]
        for pair in sample_fval_pairs[1:]:
            if pair[1] < best[1]:
                best = pair

        # optimize by iterating over collection
        # for dim in self.dim_subspaces
        while available_samples > 0:
            # print(list(range(self.min_dim, self.max_dim-self.min_dim+2)))
            # print(probability_table)
            subspace_dim = 1+np.random.choice(self.dim, size=1, p=self.probability_table)[0]
            # print(subspace_dim)
            # TODO: maybe probe count should depend on
            available_samples -= 1
            dimensions = np.random.choice(self.dim, size=subspace_dim, replace=False)
            v = np.random.uniform(size=subspace_dim) * 200 - 100
            back_point = np.copy(best[0])
            for index, sub_dim in enumerate(dimensions):
                back_point[sub_dim] = v[index]
            fv = self.cec2017(self.fn_number, back_point)[0]
            if fv < best[1]:
                best = (back_point, fv)
