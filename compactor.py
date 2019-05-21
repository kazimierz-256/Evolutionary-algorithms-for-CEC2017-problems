import sys
import time

import numpy as np
from itertools import chain

class Compactor:
    def __init__(self, cec2017, fn_number, dim, survival_rate, probes_per_iteration, limit = 100000, safety_closeness_to_past = 0.2):
        self.dim = dim
        self.cec2017 = cec2017
        self.fn_number = fn_number
        self.survival_rate = survival_rate
        self.safety_closeness_to_past = safety_closeness_to_past
        self.box_boundaries = 100
        self.probes_per_iteration = probes_per_iteration
        self.limit = limit
        self.initial_probe_count = int(probes_per_iteration/(1-survival_rate))
        
    def optimize_min(self):
        left_boundaries = np.ones(self.dim) * -self.box_boundaries
        right_boundaries = np.ones(self.dim) * self.box_boundaries
        def get_random_point(left, right):
            return left + np.multiply(right - left, np.random.uniform(size=self.dim))

        available_samples = self.limit
        # probe the space
        sample_count = min(available_samples, self.initial_probe_count)
        samples = (get_random_point(left_boundaries, right_boundaries) for _ in range(sample_count))
        available_samples -= sample_count
        sample_fval_pairs = ((v, self.cec2017(self.fn_number, v)[0]) for v in samples)
        # sort according to value
        pairs = sorted(sample_fval_pairs, key = lambda p: -p[1])

        def establish_new_boundaries(descending_pairs, previous_left, previous_right):
            # establish new boundaries
            single_dimensional_survival_rate = self.survival_rate ** (1/self.dim)
            new_left_boundaries = np.copy(descending_pairs[0][0])
            new_right_boundaries = np.copy(descending_pairs[0][0])

            survival_ratio = 0.0
            def safe_boundaries_left(left):
                diff = previous_right - previous_left
                return np.minimum(previous_left + single_dimensional_survival_rate * diff, previous_left * self.safety_closeness_to_past + left * (1.0-self.safety_closeness_to_past))
            def safe_boundaries_right(right):
                diff = previous_right - previous_left
                return np.maximum(previous_right - single_dimensional_survival_rate * diff, previous_right * self.safety_closeness_to_past + right * (1.0-self.safety_closeness_to_past))

            def boundary_survival_ratio(left, right):
                # could be the product of those, some norm of some sort
                return np.divide(left - right, previous_left - previous_right).min()

            survived = list()
            survived.append(descending_pairs[0])
            last_surviving_index = 0
            survival_ratio = 0
            # expand survival ratio
            for index, point_fval in enumerate(descending_pairs[1:]):
                if survival_ratio > single_dimensional_survival_rate:
                    break
                # expand
                new_right_boundaries = np.maximum(new_right_boundaries, point_fval[0])
                new_left_boundaries = np.minimum(new_left_boundaries, point_fval[0])
                survived.append(point_fval)
                last_surviving_index = index
                survival_ratio = boundary_survival_ratio(safe_boundaries_left(new_left_boundaries), safe_boundaries_right(new_right_boundaries))

            # pack in the remaining valid vertices
            # TODO start from index is it ok?
            for point_fval in descending_pairs[(last_surviving_index + 1):]:
                if np.less_equal(point_fval[0], new_left_boundaries).all() \
                    and np.greater_equal(new_right_boundaries, point_fval[0]).all():
                    survived.append(point_fval)
            
            return (survived, new_left_boundaries, new_right_boundaries)

        while available_samples > 0:
            new_point_count = min(available_samples, self.probes_per_iteration)
            new_points = (get_random_point(left_boundaries, right_boundaries) for _ in range(new_point_count))
            available_samples -= new_point_count
            new_points_fval = ((v, self.cec2017(self.fn_number, v)[0]) for v in new_points)
            new_pairs = sorted(chain(pairs, new_points_fval), key=lambda p: -p[1])
            survived_pairs, new_left, new_right = establish_new_boundaries(new_pairs, left_boundaries, right_boundaries)
            left_boundaries = new_left
            right_boundaries = new_right
            pairs = survived_pairs

        
