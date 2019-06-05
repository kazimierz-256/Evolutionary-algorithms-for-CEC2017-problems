import numpy as np


class Subspyce:
    def __init__(self, cec2017, fn_number, dim, limit, initial_probe_count, local_optimization_iter=0):
        '''

        :param cec2017:
        :param fn_number:
        :param dim:
        :param limit:
        :param initial_probe_count:
        :param local_optimization_iter: int
            when set to 0: there will be no local optimization.
            when set to > 0: the number indicates how many iterations of local optimization.
        '''
        self.dim = dim
        self.cec2017 = cec2017
        self.fn_number = fn_number
        self.limit = limit
        self.initial_probe_count = initial_probe_count
        self.local_optimization_iter = local_optimization_iter

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
        best_val = self.cec2017(self.fn_number, best_point)[0]
        for row in range(1, sample_count):
            point = samples[:, row]
            val = self.cec2017(self.fn_number, point)[0]
            if val < best_val:
                best_point = point
                best_val = val

        dimension = np.random.choice(self.dim, size=available_samples)
        high, low = 100., -100.
        points = np.random.uniform(low=low, high=high, size=available_samples)
        distances = [[] for _ in range(self.dim)]

        iter_since_last_update = [0 for _ in range(self.dim)]

        # global optimization
        while available_samples - self.local_optimization_iter > 0:
            available_samples -= 1
            chosen_dimension = dimension[available_samples]
            archive = best_point[chosen_dimension]
            best_point[chosen_dimension] = points[available_samples]
            fv = self.cec2017(self.fn_number, best_point)[0]
            if fv < best_val:
                # point is already modified
                best_val = fv
                distances[chosen_dimension].append(abs(archive - best_point[chosen_dimension]))
            else:
                # value should be left untouched
                best_point[chosen_dimension] = archive

        def get_point(point):
            k = np.random.random()
            if np.random.random() < 0.5:
                return point - safe_dist + (safe_dist * (((safe_dist + 100 - point) / safe_dist) ** k))
            else:
                return point + safe_dist - (safe_dist * (((safe_dist + 100 + point) / safe_dist) ** k))

        # local optimization
        safe_dist = 0.2
        while self.local_optimization_iter > 0:
            self.local_optimization_iter -= 1
            chosen_dimension = dimension[self.local_optimization_iter]
            archive = best_point[chosen_dimension]
            best_point[chosen_dimension] = get_point(archive)
            assert (-100. <= best_point[chosen_dimension] <= 100.)
            fv = self.cec2017(self.fn_number, best_point)[0]
            if fv < best_val:
                # point is already modified
                best_val = fv
                distances[chosen_dimension].append(abs(archive - best_point[chosen_dimension]))
            else:
                # value should be left untouched
                best_point[chosen_dimension] = archive
