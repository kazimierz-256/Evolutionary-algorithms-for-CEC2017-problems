import sys
import time

import numpy as np
from itertools import chain

class Compactor:
    def __init__(self, dim, cec2017, fn_number, survival_rate, probes_per_iteration):
        self.dim = dim
        self.cec2017 = cec2017
        self.fn_number = fn_number
        self.survival_rate = survival_rate
        self.safety_closeness_to_past = .2
        self.box_boundaries = 100
        self.probes_per_iteration = probes_per_iteration
        self.limit = 100_000
        self.initial_probe_count = probes_per_iteration/(1-survival_rate))
        
    def optimize_min(self):
        left_boundaries = np.ones(dim) * -self.box_boundaries
        right_boundaries = np.ones(dim) * self.box_boundaries
        def get_random_point(left, right):
            return left + np.multiply(right - left, np.random.uniform(size=dim))

        available_samples = self.limit
        # probe the space
        samples = (get_random_point(left_boundaries, right_boundaries) for _ in range(min(available_samples, self.initial_probe_count)))
        available_samples -= len(samples)
        sample_fval_pairs = ((v, self.cec2017(self.fn_number, v)[0]) for v in samples)
        # sort according to value
        sample_fval_pairs_descending_by_fval = sorted(sample_fval_pairs, key = lambda p: -p[1])


        while available_samples > 0:
            new_points = (get_random_point(left, right) for _ in range(min(available_samples, self.probes_per_iteration)))
            available_samples -= len(new_points)
            new_points_fval = ((v, self.cec2017(self.fn_number, v)[0]) for v in new_points)
            new_pairs = sorted(chain(pairs, new_points_fval), key=lambda p: -p[1])
            survived_pairs, new_left, new_right = establish_new_boundaries(new_pairs, left, right)
            left = new_left
            right = new_right
            pairs = survived_pairs

        def establish_new_boundaries(descending_pairs, previous_left, previous_right):
            # establish new boundaries
            new_left_boundaries = np.copy(descending_pairs[0][0])
            new_right_boundaries = np.copy(descending_pairs[0][0])

            survival_ratio = 0.0
            def safe_boundaries_left(left):
                previous_left * self.safety_closeness_to_past + left * (1.0-self.safety_closeness_to_past)
            def safe_boundaries_right(right):
                previous_right * self.safety_closeness_to_past + right * (1.0-self.safety_closeness_to_past)

            def boundary_survival_ratio(left, right):
                # could be the product of those
                return numpy.divide(left - right, previous_left - previous_right).min()

            survived = list()
            survived.push(descending_pairs[0])
            last_surviving_index = 0
            survival_ratio = 0

            # expand survival ratio
            for index, point_fval in enumerate(descending_pairs[1:]):
                if survival_ratio > self.survival_rate:
                    break
                # expand
                new_right_boundaries = np.maximum(new_right_boundaries, point_fval[0])
                new_left_boundaries = np.minimum(new_left_boundaries, point_fval[0])
                survived.push(point_fval)
                last_surviving_index = index
                survival_ratio = boundary_survival_ratio(safe_boundaries_left(new_left_boundaries), safe_boundaries_right(new_right_boundaries))

            # pack in the remaining valid vertices
            # TODO start from index is it ok?
            for point_fval in descending_pairs[(last_surviving_index+1):]
                if np.less_equal(point_fval[0], new_left_boundaries).all() 
                    and np.greater_equal(new_right_boundaries, point_fval[0]).all()
                    survived.push(point_fval)
            
            return (survived, new_left_boundaries, new_right_boundaries)



