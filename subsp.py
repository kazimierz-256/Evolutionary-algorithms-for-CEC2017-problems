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
        best_point = samples[:,0]
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

# import numpy as np


# class Subspyce:
#     def __init__(self, cec2017, fn_number, dim, limit, initial_probe_count):
#         self.dim = dim
#         self.cec2017 = cec2017
#         self.fn_number = fn_number
#         self.limit = limit
#         self.initial_probe_count = initial_probe_count
#         self.init_limit = int(initial_probe_count / 5)

#     def optimize_min(self):
#         available_samples = self.limit - 1

#         # choose the best one
#         best_point = np.random.uniform(size=self.dim)
#         best_val = self.cec2017(self.fn_number, best_point)[0]
#         last_time_updated = 0
#         for iterr in range(min(available_samples, self.initial_probe_count)):
#             new_rand = np.random.uniform(size=self.dim)
#             rand_val = self.cec2017(self.fn_number, new_rand)[0]
#             available_samples -= 1
#             if rand_val < best_val:
#                 best_val = rand_val
#                 best_point = new_rand
#                 last_time_updated = iterr
#             elif iterr - last_time_updated > self.init_limit:
#                 break

#         dimension = np.random.choice(self.dim, size=available_samples)
#         points = np.random.uniform(size=available_samples) * 200 - 100

#         while available_samples > 0:
#             available_samples -= 1
#             chosen_dimension = dimension[available_samples]
#             archive = best_point[chosen_dimension]
#             best_point[chosen_dimension] = points[available_samples]
#             fv = self.cec2017(self.fn_number, best_point)[0]
#             if fv < best_val:
#                 best_val = fv
#                 # point is already modified
#             else:
#                 best_point[chosen_dimension] = archive
#                 # value should be left untouched


#         # while available_samples > 0:
#         #     # TODO: maybe probe count should depend on
#         #     available_samples -= 1
#         #     dimensions = np.random.choice(self.dim, size=1, replace=False)
#         #     v = np.random.uniform(size=1) * 200 - 100
#         #     back_point = np.copy(best[0])
#         #     for index, sub_dim in enumerate(dimensions):
#         #         back_point[sub_dim] = v[index]
#         #     fv = self.cec2017(self.fn_number, back_point)[0]
#         #     if fv < best[1]:
#         #         best = (back_point, fv)
