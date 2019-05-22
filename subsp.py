import numpy as np


class Subspyce:
    def __init__(self, cec2017, fn_number, dim, limit, initial_probe_count):
        self.dim = dim
        self.cec2017 = cec2017
        self.fn_number = fn_number
        self.limit = limit
        self.initial_probe_count = initial_probe_count
        # self.probability_table = probability_table

    def optimize_min(self):
        available_samples = self.limit
        # probe the space
        sample_count = min(available_samples, self.initial_probe_count)
        available_samples -= sample_count
        samples = (np.random.uniform(size=self.dim) for _ in range(sample_count))

        # randomize initial set of points
        sample_fval_pairs = [(v, self.cec2017(self.fn_number, v)[0]) for v in samples]

        # choose the best one
        best_point = sample_fval_pairs[0][0]
        best_val = sample_fval_pairs[0][1]
        for pair in sample_fval_pairs[1:]:
            if pair[1] < best_val:
                best_val = pair[1]
                best_point = pair[0]

        dimension = np.random.choice(self.dim, size=available_samples)
        points = np.random.uniform(size=available_samples) * 200 - 100

        while available_samples > 0:
            available_samples -= 1
            chosen_dimension = dimension[available_samples]
            archive = best_point[chosen_dimension]
            best_point[chosen_dimension] = points[available_samples]
            fv = self.cec2017(self.fn_number, best_point)[0]
            if fv < best_val:
                best_val = fv
                # point is already modified
            else:
                best_point[chosen_dimension] = archive
                # value should be left untouched
