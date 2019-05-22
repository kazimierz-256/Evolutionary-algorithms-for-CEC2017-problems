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
        samples = np.random.uniform(low=-100.0, high=100.0, size=(self.dim, sample_count))

        # randomize initial set of points
        # sample_fval_pairs = [(v, self.cec2017(self.fn_number, v)[0]) for v in samples]

        # choose the best one
        # print(samples[0])
        best_point = samples[:, 0]
        # print(best_point)
        best_val = self.cec2017(self.fn_number, best_point)[0]
        for row in range(1, sample_count):
            point = samples[:, row]
            val = self.cec2017(self.fn_number, point)[0]
            if val < best_val:
                best_point = point
                best_val = val

        dimension = np.random.choice(self.dim, size=available_samples)
        points = np.random.uniform(low=-100.0, high=100.0, size=available_samples)

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
