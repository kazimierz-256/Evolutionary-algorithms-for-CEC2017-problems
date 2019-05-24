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
                iter_since_last_update[chosen_dimension] = 0
            else:
                # value should be left untouched
                best_point[chosen_dimension] = archive
                iter_since_last_update[chosen_dimension] += 1

        coef = .2
        high_lows = [(high, low) for _ in range(self.dim)]

        def get_point(high_low):
            high, low = high_low
            return np.random.uniform(low=low, high=high)

        def change_high_lows(high_lows, dim, coef, mean):
            high, low = high_lows[dim]
            # print("old_high_low", high, low)
            new_len = (high - low) * coef
            high_lows[dim] = min(100., mean + new_len / 2.), max(-100., mean - new_len / 2.)
            # print("new_high_low", high_lows[dim])
            return high_lows

        def shrink_high_lows(high_lows, dim, coef, mean):
            # print("shrink", dim)
            return change_high_lows(high_lows, dim, 1 - coef, mean)

        def widen_high_lows(high_lows, dim, coef, mean):
            # print("widen", dim)
            return change_high_lows(high_lows, dim, 1 + coef, mean)

        # print("local_optim")
        # local optimization
        while self.local_optimization_iter > 0:
            self.local_optimization_iter -= 1
            chosen_dimension = dimension[self.local_optimization_iter]
            archive = best_point[chosen_dimension]
            best_point[chosen_dimension] = get_point(high_lows[chosen_dimension])
            fv = self.cec2017(self.fn_number, best_point)[0]
            if fv < best_val:
                # point is already modified
                best_val = fv
                iter_since_last_update[chosen_dimension] = 0
                high_lows = widen_high_lows(high_lows, chosen_dimension, coef, best_point[chosen_dimension])
            else:
                # value should be left untouched
                best_point[chosen_dimension] = archive
                iter_since_last_update[chosen_dimension] += 1

            if iter_since_last_update[chosen_dimension] >= 1000:
                high_lows = shrink_high_lows(high_lows, chosen_dimension, coef, best_point[chosen_dimension])
                iter_since_last_update[chosen_dimension] = 0
